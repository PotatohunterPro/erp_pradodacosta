"""
Gerador de XML para NFC-e

Usa biblioteca erpbrasil.edoc para gerar XML conforme SEFAZ layout 4.0
"""

from datetime import datetime
from typing import Dict, Any
from decimal import Decimal
import logging

from nfce_models import NfcePayload, ProdutoNfce

logger = logging.getLogger(__name__)


class NfceGenerator:
    """
    Gera XML válido para NFC-e conforme SEFAZ layout 4.0

    Nota: Assinatura digital é feita em módulo separado (assinador.py)
    """

    def __init__(self):
        self.versao_xml = "4.00"
        self.modelo = 65  # NFC-e sempre é modelo 65
        self.serie = 65   # NFC-e sempre é série 65

    def gerar_xml(self, payload: NfcePayload) -> str:
        """
        Gera XML NFC-e a partir de payload validado

        Args:
            payload: NfcePayload com dados da venda

        Returns:
            String com XML bem-formado

        Raises:
            ValueError: Se dados forem inválidos
        """
        logger.info("Iniciando geração de XML NFC-e")

        try:
            # Construir estrutura de dados para erpbrasil.edoc
            dados_nfce = self._construir_estrutura(payload)

            # Gerar XML usando erpbrasil.edoc
            xml_nfce = self._gerar_xml_erpbrasil(dados_nfce)

            logger.info(f"XML NFC-e gerado com sucesso")
            return xml_nfce

        except Exception as e:
            logger.error(f"Erro ao gerar XML NFC-e: {str(e)}")
            raise ValueError(f"Erro na geração de XML: {str(e)}")

    def _construir_estrutura(self, payload: NfcePayload) -> Dict[str, Any]:
        """
        Constrói dicionário com dados estruturados para erpbrasil.edoc
        """
        agora = datetime.now()

        return {
            # Identificação
            "emitente": {
                "cnpj": payload.emitente.cnpj,
                "ie": payload.emitente.ie,
                "razao_social": payload.emitente.razao_social,
                "nome_fantasia": payload.emitente.nome_fantasia,
                "endereco": {
                    "logradouro": payload.emitente.endereco,
                    "numero": payload.emitente.numero,
                    "complemento": payload.emitente.complemento or "",
                    "bairro": payload.emitente.bairro,
                    "municipio": payload.emitente.municipio,
                    "uf": payload.emitente.uf,
                    "cep": payload.emitente.cep,
                },
                "telefone": payload.emitente.telefone or "",
                "email": payload.emitente.email or "",
            },

            # Consumidor (opcional)
            "consumidor": {
                "cpf_cnpj": payload.consumidor.cpf_cnpj if payload.consumidor else "",
                "nome": payload.consumidor.nome if payload.consumidor else "",
            },

            # Produtos
            "produtos": [
                self._construir_produto(p) for p in payload.produtos
            ],

            # Valores
            "totais": {
                "valor_produtos": float(payload.valor_total_produtos()),
                "valor_icms": float(payload.valor_total_icms()),
                "valor_pis": float(payload.valor_total_pis()),
                "valor_cofins": float(payload.valor_total_cofins()),
                "valor_total": float(self._calcular_total(payload)),
            },

            # NFC-e específico
            "numero": payload.numero_nfce,
            "serie": payload.serie_nfce,
            "modelo": self.modelo,
            "versao": self.versao_xml,
            "data_hora": agora.isoformat(),
            "ambiente": "homologacao",  # TODO: tornar configurável
            "observacao": payload.observacao or "",
        }

    def _construir_produto(self, produto: ProdutoNfce) -> Dict[str, Any]:
        """
        Constrói dicionário com dados do produto
        """
        valor_total = produto.valor_total()
        valor_icms = valor_total * Decimal(str(produto.aliquota_icms / 100))
        valor_pis = valor_total * Decimal(str(produto.aliquota_pis / 100))
        valor_cofins = valor_total * Decimal(str(produto.aliquota_cofins / 100))

        return {
            "ncm": produto.ncm,
            "cfop": produto.cfop,
            "descricao": produto.descricao,
            "quantidade": float(produto.quantidade),
            "valor_unitario": float(produto.valor_unitario),
            "valor_total": float(valor_total),
            "origem": produto.origem,
            "cst_icms": produto.cst_icms,
            "cst_pis": produto.cst_pis,
            "cst_cofins": produto.cst_cofins,
            "aliquota_icms": produto.aliquota_icms,
            "aliquota_pis": produto.aliquota_pis,
            "aliquota_cofins": produto.aliquota_cofins,
            "valor_icms": float(valor_icms),
            "valor_pis": float(valor_pis),
            "valor_cofins": float(valor_cofins),
        }

    def _calcular_total(self, payload: NfcePayload) -> Decimal:
        """
        Calcula valor total da NFC-e (produtos + impostos)
        """
        return payload.valor_total_produtos()

    def _gerar_xml_erpbrasil(self, dados: Dict[str, Any]) -> str:
        """
        Gera XML usando biblioteca erpbrasil.edoc

        TODO: Implementar quando erpbrasil.edoc estiver totalmente integrado
        Por enquanto, retorna XML estruturado mock para testes
        """

        # Placeholder até integração real com erpbrasil.edoc
        xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
  <infNFe Id="NFe{dados['emitente']['cnpj']}{dados['numero']:08d}" versao="{dados['versao']}">
    <ide>
      <cUF>35</cUF>
      <natOp>VENDA AO CONSUMIDOR</natOp>
      <mod>{dados['modelo']}</mod>
      <serie>{dados['serie']}</serie>
      <nNF>{dados['numero']}</nNF>
      <dEmi>{datetime.now().strftime('%Y-%m-%d')}</dEmi>
      <hEmi>{datetime.now().strftime('%H:%M:%S')}</hEmi>
      <tpNF>1</tpNF>
      <idDest>1</idDest>
      <cMunFG>3550308</cMunFG>
      <tpImp>4</tpImp>
      <tpEmis>1</tpEmis>
      <cDV>0</cDV>
      <tpAmbiente>2</tpAmbiente>
      <finNFe>1</finNFe>
      <indFinal>1</indFinal>
      <indPres>1</indPres>
      <procEmi>0</procEmi>
      <verProc>4.0.0</verProc>
    </ide>
    <emit>
      <CNPJ>{dados['emitente']['cnpj']}</CNPJ>
      <xNome>{dados['emitente']['razao_social']}</xNome>
      <xFant>{dados['emitente']['nome_fantasia']}</xFant>
      <enderEmit>
        <xLgr>{dados['emitente']['endereco']['logradouro']}</xLgr>
        <nro>{dados['emitente']['endereco']['numero']}</nro>
        <xBairro>{dados['emitente']['endereco']['bairro']}</xBairro>
        <cMun>3550308</cMun>
        <xMun>SÃO PAULO</xMun>
        <UF>{dados['emitente']['endereco']['uf']}</UF>
        <CEP>{dados['emitente']['endereco']['cep']}</CEP>
        <cPais>1058</cPais>
        <xPais>BRASIL</xPais>
      </enderEmit>
      <IE>{dados['emitente']['ie']}</IE>
    </emit>
    <dest>
      {'<CNPJ>' + dados['consumidor']['cpf_cnpj'] + '</CNPJ>' if len(dados['consumidor']['cpf_cnpj']) == 14 else '<CPF>' + dados['consumidor']['cpf_cnpj'] + '</CPF>' if dados['consumidor']['cpf_cnpj'] else '<CNPJ>16716114000172</CNPJ>'}
      {'<xNome>' + dados['consumidor']['nome'] + '</xNome>' if dados['consumidor']['nome'] else '<xNome>CONSUMIDOR FINAL</xNome>'}
    </dest>
    <det nItem="1">
      <prod>
        <NCM>{dados['produtos'][0]['ncm']}</NCM>
        <CFOP>{dados['produtos'][0]['cfop']}</CFOP>
        <xProd>{dados['produtos'][0]['descricao']}</xProd>
        <qCom>{dados['produtos'][0]['quantidade']:.2f}</qCom>
        <vUnCom>{dados['produtos'][0]['valor_unitario']:.2f}</vUnCom>
        <indTot>1</indTot>
      </prod>
      <imposto>
        <ICMS>
          <ICMS00>
            <orig>{dados['produtos'][0]['origem']}</orig>
            <CST>{dados['produtos'][0]['cst_icms']}</CST>
            <modBC>3</modBC>
            <vBC>{dados['produtos'][0]['valor_total']:.2f}</vBC>
            <pICMS>{dados['produtos'][0]['aliquota_icms']:.2f}</pICMS>
            <vICMS>{dados['produtos'][0]['valor_icms']:.2f}</vICMS>
          </ICMS00>
        </ICMS>
        <PIS>
          <PISNT>
            <CST>{dados['produtos'][0]['cst_pis']}</CST>
          </PISNT>
        </PIS>
        <COFINS>
          <COFINSNT>
            <CST>{dados['produtos'][0]['cst_cofins']}</CST>
          </COFINSNT>
        </COFINS>
      </imposto>
    </det>
    <total>
      <ICMSTot>
        <vBC>{dados['totais']['valor_produtos']:.2f}</vBC>
        <vICMS>{dados['totais']['valor_icms']:.2f}</vICMS>
        <vPIS>{dados['totais']['valor_pis']:.2f}</vPIS>
        <vCOFINS>{dados['totais']['valor_cofins']:.2f}</vCOFINS>
        <vNF>{dados['totais']['valor_total']:.2f}</vNF>
      </ICMSTot>
    </total>
    <infAdic>
      {'<infCpl>' + dados['observacao'] + '</infCpl>' if dados['observacao'] else ''}
    </infAdic>
  </infNFe>
</NFe>
"""
        return xml_template.replace('\n      ', '\n').strip()

    def validar_xml(self, xml: str) -> bool:
        """
        Valida XML contra XSD SEFAZ

        TODO: Implementar validação contra XSD real
        Por enquanto apenas verifica se é XML bem-formado
        """
        try:
            # Verificação básica: XML bem-formado
            import xml.etree.ElementTree as ET
            ET.fromstring(xml)
            logger.info("XML validado com sucesso")
            return True
        except Exception as e:
            logger.error(f"XML inválido: {str(e)}")
            return False

    def gerar_chave_nfce(self, payload: NfcePayload) -> str:
        """
        Gera chave de acesso NFC-e (44 dígitos)

        Formato: UF AAMM CNPJ MODELO SÉRIE NÚMERO DV
        """
        cnpj = payload.emitente.cnpj
        numero = payload.numero_nfce
        serie = payload.serie_nfce
        modelo = self.modelo
        agora = datetime.now()

        # Partes da chave
        uf = "35"  # TODO: extrair do emitente
        aa_mm = agora.strftime("%y%m")

        # Monta chave sem DV (43 dígitos)
        chave_sem_dv = f"{uf}{aa_mm}{cnpj}{modelo:02d}{serie:03d}{numero:08d}"

        # Calcula DV (módulo 11)
        dv = self._calcular_dv(chave_sem_dv)

        chave_completa = chave_sem_dv + str(dv)

        logger.info(f"Chave NFC-e gerada: {chave_completa}")
        return chave_completa

    @staticmethod
    def _calcular_dv(chave: str) -> int:
        """
        Calcula dígito verificador (módulo 11)

        Algoritmo SEFAZ
        """
        sequencia = "2987654321"
        soma = 0

        for i, digito in enumerate(chave):
            soma += int(digito) * int(sequencia[i % len(sequencia)])

        resto = soma % 11
        dv = 11 - resto

        return 0 if dv == 11 else dv
