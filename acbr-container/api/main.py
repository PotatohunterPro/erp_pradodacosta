"""
API REST - Serviços Fiscais Brasileiros
Usa erpbrasil.edoc (100% Python, sem ACBrLib)

Funcionalidades:
- NF-e (Nota Fiscal Eletrônica) via erpbrasil.edoc
- NFC-e (Cupom Fiscal Eletrônico) via erpbrasil.edoc
- DANFE em PDF via reportlab
- Validação CPF/CNPJ
- Consulta IBPT
- QR Code NFC-e
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os, sys

# Adicionar diretório de módulos ao path
sys.path.insert(0, os.path.dirname(__file__))

app = FastAPI(
    title="Serviços Fiscais Brasileiros - ERP Prado da Costa",
    description="API fiscal usando erpbrasil.edoc (NF-e, NFC-e, DANFE, validações)",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================
# Modelos
# ============================================================

class NFeConfig(BaseModel):
    certificado_path: str = "/opt/acbr/certificados"
    certificado_senha: str = ""
    uf: str = "SP"
    ambiente: str = "homologacao"  # homologacao | producao
    cnpj_emitente: str = ""
    ie_emitente: str = ""
    crt: int = 1  # 1=Simples Nacional, 2=Simples Excesso, 3=Regime Normal
    serie: int = 1
    versao: str = "4.00"

class ProdutoNota(BaseModel):
    codigo: str
    descricao: str
    ncm: str = "00000000"
    cfop: str = "5102"
    unidade: str = "UN"
    quantidade: float = 1.0
    valor_unitario: float = 0.0
    valor_total: float = 0.0

class EmitirNFeRequest(BaseModel):
    config: NFeConfig = NFeConfig()
    destinatario_nome: str = "CONSUMIDOR"
    destinatario_cpf_cnpj: str = "00000000000"
    destinatario_ie: str = ""
    produtos: list[ProdutoNota] = []
    valor_frete: float = 0.0
    valor_seguro: float = 0.0
    valor_desconto: float = 0.0
    forma_pagamento: str = "01"  # 01=Dinheiro, 03=Cartão, 99=Outros
    informacoes_complementares: str = ""

class StatusResponse(BaseModel):
    status: str = "ok"
    versao_api: str = "2.0.0"
    bibliotecas: dict = {}

class ResultadoNFe(BaseModel):
    sucesso: bool
    chave_acesso: Optional[str] = None
    numero: Optional[int] = None
    protocolo: Optional[str] = None
    xml_assinado: Optional[str] = None
    danfe_base64: Optional[str] = None
    erros: list[str] = []

class ResultadoNFCe(BaseModel):
    sucesso: bool
    chave_acesso: Optional[str] = None
    protocolo: Optional[str] = None
    qrcode_url: Optional[str] = None
    xml_assinado: Optional[str] = None
    erros: list[str] = []

class ResultadoValidacao(BaseModel):
    valido: bool
    tipo: Optional[str] = None
    formatado: Optional[str] = None
    mensagem: Optional[str] = None


# ============================================================
# Endpoints
# ============================================================

@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Verifica se o serviço está rodando e as bibliotecas disponíveis"""
    biblio = {"erpbrasil_edoc": False, "cryptography": False, "reportlab": False, "qrcode": False}
    
    try:
        import erpbrasil.edoc
        biblio["erpbrasil_edoc"] = True
        biblio["erpbrasil_edoc_version"] = erpbrasil.edoc.__version__
    except:
        pass
    
    try:
        from cryptography import x509
        biblio["cryptography"] = True
    except:
        pass
    
    try:
        import reportlab
        biblio["reportlab"] = True
    except:
        pass
    
    try:
        import qrcode
        biblio["qrcode"] = True
    except:
        pass
    
    return StatusResponse(
        versao_api="2.0.0",
        bibliotecas=biblio,
    )

@app.post("/nfe/emitir", response_model=ResultadoNFe)
async def nfe_emitir(request: EmitirNFeRequest):
    """
    Gera e transmite NF-e usando erpbrasil.edoc
    """
    try:
        from .nfe_controller import emitir_nfe_via_edoc
        return emitir_nfe_via_edoc(request)
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail=f"Biblioteca erpbrasil.edoc não disponível. Instale com: pip install erpbrasil.edoc. Erro: {e}"
        )

@app.get("/nfe/consultar", response_model=ResultadoNFe)
async def nfe_consultar(chave_acesso: str):
    """Consulta situação de NF-e na SEFAZ"""
    try:
        from .nfe_controller import consultar_nfe_via_edoc
        return consultar_nfe_via_edoc(chave_acesso)
    except ImportError:
        raise HTTPException(status_code=501, detail="erpbrasil.edoc não disponível")

@app.post("/nfe/cancelar", response_model=ResultadoNFe)
async def nfe_cancelar(chave_acesso: str, justificativa: str, protocolo: str):
    """Cancela NF-e na SEFAZ"""
    try:
        from .nfe_controller import cancelar_nfe_via_edoc
        return cancelar_nfe_via_edoc(chave_acesso, justificativa, protocolo)
    except ImportError:
        raise HTTPException(status_code=501, detail="erpbrasil.edoc não disponível")

@app.post("/nfce/emitir", response_model=ResultadoNFCe)
async def nfce_emitir(request: EmitirNFeRequest):
    """
    Gera e transmite NFC-e (cupom fiscal eletrônico)
    """
    try:
        from .nfce_controller import emitir_nfce_via_edoc
        return emitir_nfce_via_edoc(request)
    except ImportError as e:
        raise HTTPException(
            status_code=501,
            detail=f"erpbrasil.edoc não disponível. Erro: {e}"
        )

@app.post("/validar/documento", response_model=ResultadoValidacao)
async def validar_documento(documento: str, tipo: str = "auto"):
    """
    Valida CPF ou CNPJ
    Implementação 100% Python (não requer erpbrasil)
    """
    from .validadores import validar_cpf, validar_cnpj
    from .formatadores import formatar_cpf, formatar_cnpj

    doc = documento.replace(".", "").replace("/", "").replace("-", "").replace(" ", "")

    if tipo == "auto":
        tipo = "cnpj" if len(doc) == 14 else "cpf" if len(doc) == 11 else None
        if not tipo:
            raise HTTPException(status_code=400, detail="Documento deve ter 11 (CPF) ou 14 (CNPJ) dígitos")

    if tipo == "cpf":
        valido, msg = validar_cpf(doc)
        formatado = formatar_cpf(doc) if valido else doc
    elif tipo == "cnpj":
        valido, msg = validar_cnpj(doc)
        formatado = formatar_cnpj(doc) if valido else doc
    else:
        raise HTTPException(status_code=400, detail=f"Tipo inválido: {tipo}")

    return ResultadoValidacao(
        valido=valido,
        tipo=tipo.upper(),
        formatado=formatado,
        mensagem=msg,
    )

@app.post("/danfe/gerar")
async def gerar_danfe(chave_acesso: str, xml_nota: str):
    """Gera DANFE em PDF a partir do XML da NF-e"""
    try:
        from .danfe_controller import gerar_danfe_pdf
        return gerar_danfe_pdf(chave_acesso, xml_nota)
    except ImportError:
        raise HTTPException(status_code=501, detail="reportlab não disponível")

@app.get("/ncm/{ncm}")
async def consultar_ncm(ncm: str):
    """Consulta descrição do NCM"""
    from .tabelas_ncm import consultar_ncm
    resultado = consultar_ncm(ncm)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"NCM {ncm} não encontrado")
    return resultado

@app.get("/cfop/{cfop}")
async def consultar_cfop(cfop: str):
    """Consulta descrição do CFOP"""
    from .tabelas_cfop import consultar_cfop
    resultado = consultar_cfop(cfop)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"CFOP {cfop} não encontrado")
    return resultado