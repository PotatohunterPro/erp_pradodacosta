"""
ACBr Bridge - Interface Python para comunicação com o container ACBrLib

Esta bridge permite que o ERPNext se comunique com a API ACBr para:
- Emissão de NF-e / NFC-e
- Consulta de status SEFAZ
- Cancelamento de notas fiscais
- Validação de CPF/CNPJ
- Consulta IBPT
- Geração de DANFE
"""

import frappe
import requests
import json
from typing import Optional
from frappe import _

# Configuração padrão - sobrescrita pelas POS Settings
ACBR_DEFAULT_HOST = frappe.conf.get("acbr_host") or "acbr"
ACBR_DEFAULT_PORT = frappe.conf.get("acbr_port") or "8080"
ACBR_BASE_URL = f"http://{ACBR_DEFAULT_HOST}:{ACBR_DEFAULT_PORT}"


# ============================================================
# Exceções
# ============================================================

class ACBrError(Exception):
    """Erro base do ACBr"""
    pass

class ACBrConnectionError(ACBrError):
    """Erro de conexão com o container ACBr"""
    pass

class ACBrValidationError(ACBrError):
    """Erro de validação (ex: CPF inválido)"""
    pass

class NFeError(ACBrError):
    """Erro relacionado à emissão de NF-e"""
    pass


# ============================================================
# Cliente HTTP para ACBr
# ============================================================

class ACBrClient:
    """Cliente HTTP para comunicação com a API ACBr"""

    def __init__(self, base_url: str = ACBR_BASE_URL, timeout: int = 30):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, endpoint: str, **kwargs) -> dict:
        """Faz requisição HTTP para a API ACBr"""
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        try:
            response = self.session.request(
                method=method,
                url=url,
                timeout=self.timeout,
                **kwargs,
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.ConnectionError as e:
            raise ACBrConnectionError(
                f"Não foi possível conectar ao ACBr em {self.base_url}. "
                f"Verifique se o container acbr está rodando. Erro: {e}"
            )
        except requests.exceptions.Timeout:
            raise ACBrConnectionError(
                f"Timeout ao conectar com ACBr em {self.base_url} "
                f"(timeout={self.timeout}s)"
            )
        except requests.exceptions.HTTPError as e:
            raise ACBrError(f"Erro HTTP do ACBr: {e}")

    def health_check(self) -> dict:
        """Verifica se o ACBr está saudável"""
        return self._request("GET", "/health")

    # ---- NF-e ----

    def emitir_nfe(self, xml_nota: str, ambiente: str = "homologacao") -> dict:
        """Emite uma NF-e"""
        return self._request(
            "POST",
            "/nfe/emitir",
            json={
                "config": {"ambiente": ambiente},
                "xml_nota": xml_nota,
            },
        )

    def consultar_nfe(self, chave_acesso: str) -> dict:
        """Consulta situação de NF-e na SEFAZ"""
        return self._request(
            "POST",
            "/nfe/consultar",
            json={"chave_acesso": chave_acesso},
        )

    def cancelar_nfe(self, chave_acesso: str, justificativa: str, protocolo: str) -> dict:
        """Cancela uma NF-e"""
        return self._request(
            "POST",
            "/nfe/cancelar",
            json={
                "chave_acesso": chave_acesso,
                "justificativa": justificativa,
                "protocolo_autorizacao": protocolo,
            },
        )

    # ---- NFC-e ----

    def emitir_nfce(self, xml_cupom: str, ambiente: str = "homologacao") -> dict:
        """Emite uma NFC-e (cupom fiscal eletrônico)"""
        return self._request(
            "POST",
            "/nfce/emitir",
            json={
                "config": {"ambiente": ambiente},
                "xml_cupom": xml_cupom,
            },
        )

    # ---- Utilitários ----

    def validar_documento(self, documento: str) -> dict:
        """Valida CPF ou CNPJ"""
        return self._request(
            "POST",
            "/validar/documento",
            json={"documento": documento},
        )

    def consultar_ibpt(self, ncm: str, uf: str = "SP", valor: float = 0.0) -> dict:
        """Consulta alíquotas IBPT para um NCM"""
        return self._request(
            "GET",
            f"/ibpt/consultar",
            params={"ncm": ncm, "uf": uf, "valor_produto": valor},
        )

    def consultar_ncm(self, ncm: str) -> dict:
        """Consulta descrição de NCM"""
        return self._request("GET", f"/ncm/{ncm}")

    def consultar_cfop(self, cfop: str) -> dict:
        """Consulta descrição de CFOP"""
        return self._request("GET", f"/cfop/{cfop}")


# ============================================================
# Singleton
# ============================================================

_cliente: Optional[ACBrClient] = None

def get_acbr_client() -> ACBrClient:
    """Retorna instância singleton do cliente ACBr"""
    global _cliente
    if _cliente is None:
        host = frappe.conf.get("acbr_host") or ACBR_DEFAULT_HOST
        port = frappe.conf.get("acbr_port") or ACBR_DEFAULT_PORT
        base_url = f"http://{host}:{port}"
        _cliente = ACBrClient(base_url=base_url)
    return _cliente


# ============================================================
# Funções de alto nível para uso nos controllers
# ============================================================

def validar_cpf_cnpj_remoto(documento: str) -> dict:
    """Valida CPF/CNPJ via ACBr (com fallback local)"""
    try:
        client = get_acbr_client()
        return client.validar_documento(documento)
    except ACBrConnectionError:
        # Fallback: validação local
        from .validadores import validar_cpf, validar_cnpj
        from .formatadores import formatar_cpf, formatar_cnpj

        doc = documento.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")
        
        if len(doc) == 11:
            valido, msg = validar_cpf(doc)
            formatado = formatar_cpf(doc) if valido else doc
            return {"valido": valido, "tipo": "CPF", "formatado": formatado, "mensagem": msg}
        elif len(doc) == 14:
            valido, msg = validar_cnpj(doc)
            formatado = formatar_cnpj(doc) if valido else doc
            return {"valido": valido, "tipo": "CNPJ", "formatado": formatado, "mensagem": msg}
        else:
            return {"valido": False, "tipo": None, "formatado": doc, "mensagem": "Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos"}