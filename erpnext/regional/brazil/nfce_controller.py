"""
Controller NFC-e - Integração da POS Invoice com NFC-e (Cupom Fiscal Eletrônico)

Este módulo intercepta o fluxo de submissão da POS Invoice para:
1. Coletar dados da venda
2. Gerar XML da NFC-e
3. Enviar para ACBrLib assinar e transmitir
4. Armazenar chave de acesso, protocolo e QR Code na fatura
"""

import frappe
from frappe import _
from typing import Optional

from erpnext.regional.brazil.acbr_bridge import get_acbr_client, ACBrConnectionError, ACBrError


class NFCeController:
    """Controller para emissão de NFC-e a partir de uma POS Invoice"""

    def __init__(self, pos_invoice):
        self.pos_invoice = pos_invoice
        self.doc = frappe.get_doc("POS Invoice", pos_invoice)

    def emitir_nfce(self):
        """
        Emite NFC-e para a POS Invoice.
        Chamado automaticamente após submissão da fatura.
        """
        if self.doc.chave_acesso_nfce:
            frappe.msgprint(_("NFC-e já foi emitida para esta fatura"))
            return

        if self.doc.docstatus != 1:  # Apenas faturas submetidas
            frappe.throw(_("A fatura precisa estar submetida para emitir NFC-e"))

        try:
            # 1. Gerar XML da NFC-e
            xml_nfce = self._gerar_xml_nfce()

            # 2. Enviar para ACBr processar
            client = get_acbr_client()
            resultado = client.emitir_nfce(xml_nfce)

            # 3. Salvar resultado na POS Invoice
            if resultado.get("sucesso"):
                self._salvar_resultado(resultado)
                frappe.msgprint(
                    _("NFC-e emitida com sucesso! Chave: {0}").format(
                        resultado.get("chave_acesso", "")
                    )
                )
            else:
                erros = "; ".join(resultado.get("erros", []))
                frappe.throw(_("Falha ao emitir NFC-e: {0}").format(erros))

        except ACBrConnectionError as e:
            frappe.throw(
                _("Não foi possível conectar ao serviço ACBr. "
                  "Verifique se o container acbr está rodando. Erro: {0}").format(str(e))
            )
        except ACBrError as e:
            frappe.throw(_("Erro ao emitir NFC-e: {0}").format(str(e)))

    def _gerar_xml_nfce(self) -> str:
        """
        Gera XML da NFC-e a partir dos dados da POS Invoice.
        
        NOTA: Esta é uma implementação inicial simplificada.
        A implementação completa usará o ACBrLib ou uma biblioteca 
        como erpbrasil.edoc para gerar o XML no padrão 4.0 da SEFAZ.
        
        TODO: Implementar geração completa do XML 4.0 com:
        - Dados do emitente (CNPJ, IE, regime tributário)
        - Dados do destinatário (CPF/CNPJ, nome, endereço)
        - Produtos (NCM, CFOP, CST, alíquotas)
        - Cálculo de impostos (ICMS, PIS, COFINS)
        - Totais, transporte, cobrança
        - Informações complementares
        """
        # Placeholder - na implementação real, gerar XML completo
        xml_template = f"""<?xml version="1.0" encoding="UTF-8"?>
<NFe xmlns="http://www.portalfiscal.inf.br/nfe">
    <infNFe Id="NFe{self.doc.name}" versao="4.00">
        <ide>
            <cUF>35</cUF>
            <cNF>00000001</cNF>
            <natOp>VENDA</natOp>
            <mod>65</mod>
            <serie>1</serie>
            <nNF>{self.doc.name}</nNF>
            <dhEmi>{self.doc.posting_date}T{self.doc.posting_time or '00:00:00'}-03:00</dhEmi>
            <tpNF>1</tpNF>
            <idDest>1</idDest>
            <tpImp>4</tpImp>
            <tpEmis>1</tpEmis>
            <cDV>0</cDV>
            <tpAmb>2</tpAmb>
            <finNFe>1</finNFe>
            <indFinal>1</indFinal>
            <indPres>1</indPres>
            <procEmi>0</procEmi>
            <verProc>ERPNext PDV 1.0</verProc>
        </ide>
        <emit>
            <CNPJ>{frappe.db.get_value("Company", self.doc.company, "tax_id") or '00000000000000'}</CNPJ>
            <xNome>{frappe.db.get_value("Company", self.doc.company, "company_name")}</xNome>
            <CRT>1</CRT>
        </emit>
        <dest>
            <CPF>{self.doc.cpf_cnpj_consumidor or '00000000000'}</CPF>
            <xNome>CONSUMIDOR</xNome>
        </dest>
        <det n="1">
            <prod>
                <cProd>001</cProd>
                <xProd>Produto</xProd>
                <NCM>00000000</NCM>
                <CFOP>5102</CFOP>
                <uCom>UN</uCom>
                <qCom>1.00</qCom>
                <vUnCom>0.00</vUnCom>
                <vProd>0.00</vProd>
                <indTot>1</indTot>
            </prod>
            <imposto>
                <vTotTrib>0.00</vTotTrib>
            </imposto>
        </det>
        <total>
            <ICMSTot>
                <vBC>0.00</vBC>
                <vICMS>0.00</vICMS>
                <vICMSDeson>0.00</vICMSDeson>
                <vFCP>0.00</vFCP>
                <vBCST>0.00</vBCST>
                <vST>0.00</vST>
                <vProd>0.00</vProd>
                <vFrete>0.00</vFrete>
                <vSeg>0.00</vSeg>
                <vDesc>0.00</vDesc>
                <vII>0.00</vII>
                <vIPI>0.00</vIPI>
                <vIPIDevol>0.00</vIPIDevol>
                <vPIS>0.00</vPIS>
                <vCOFINS>0.00</vCOFINS>
                <vOutro>0.00</vOutro>
                <vNF>{self.doc.grand_total}</vNF>
                <vTotTrib>0.00</vTotTrib>
            </ICMSTot>
        </total>
        <pag>
            <detPag>
                <tPag>01</tPag>
                <vPag>{self.doc.grand_total}</vPag>
            </detPag>
        </pag>
    </infNFe>
</NFe>"""
        return xml_template

    def _salvar_resultado(self, resultado: dict):
        """Salva os dados da NFC-e na POS Invoice"""
        campos_atualizar = {
            "chave_acesso_nfce": resultado.get("chave_acesso"),
            "protocolo_nfce": resultado.get("protocolo"),
            "qr_code_nfce": resultado.get("qrcode_url"),
            "xml_nfce": resultado.get("xml_assinado"),
        }
        frappe.db.set_value(
            "POS Invoice",
            self.doc.name,
            campos_atualizar,
        )


def emitir_nfce_para_pos_invoice(doc, method=None):
    """
    Hook para ser chamado automaticamente após submissão da POS Invoice.
    Registre este hook em hooks.py:
        doc_events = {
            "POS Invoice": {
                "on_submit": "erpnext.regional.brazil.nfce_controller.emitir_nfce_para_pos_invoice"
            }
        }
    """
    # Verificar se configuração Brasil está ativa
    if not frappe.db.get_value("Company", doc.company, "country") == "Brazil":
        return

    # Verificar se NFC-e automática está ativa
    # TODO: Adicionar flag em POS Settings "emitir_nfce_automaticamente"
    
    controller = NFCeController(doc.name)
    controller.emitir_nfce()