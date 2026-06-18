"""
Setup do módulo regional Brasil para ERPNext

Configura:
- Plano de contas brasileiro
- Doctypes fiscais (CFOP, NCM, CEST)
- Campos personalizados em Item, Customer, Sales Invoice
- Impressão fiscal
- Integração com ACBrLib
"""

import frappe
from frappe import _

def setup_brazil():
    """Configura o módulo Brasil para uma empresa"""
    frappe.log_error("Configurando módulo regional Brasil...", "Brazil Setup")
    
    setup_custom_fields()
    setup_print_formats()
    setup_accounts()
    
    frappe.log_error("Módulo regional Brasil configurado com sucesso!", "Brazil Setup")

def after_install():
    """Executado após instalação do app"""
    frappe.log_error("Módulo Brazil instalado!", "Brazil Install")


def setup_custom_fields():
    """Adiciona campos fiscais brasileiros nos doctypes"""
    from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
    
    custom_fields = {
        "Item": [
            {
                "fieldname": "ncm",
                "label": "NCM",
                "fieldtype": "Char",
                "length": 8,
                "insert_after": "item_code",
                "description": "Nomenclatura Comum do Mercosul (8 dígitos)",
            },
            {
                "fieldname": "cest",
                "label": "CEST",
                "fieldtype": "Char",
                "length": 7,
                "insert_after": "ncm",
                "description": "Código Especificador da Substituição Tributária",
            },
            {
                "fieldname": "cfop_default",
                "label": "CFOP Padrão",
                "fieldtype": "Char",
                "length": 4,
                "insert_after": "cest",
                "description": "Código Fiscal de Operações e Prestações padrão para este item",
            },
            {
                "fieldname": "origem_mercadoria",
                "label": "Origem da Mercadoria",
                "fieldtype": "Select",
                "options": "\n0 - Nacional\n1 - Estrangeira - Importação Direta\n2 - Estrangeira - Adquirida no Mercado Interno\n3 - Nacional - Conteúdo Importado > 40%\n4 - Nacional - Produção Conforme Processo Produtivo Básico\n5 - Nacional - Conteúdo Importado <= 40%\n6 - Estrangeira - Importação Direta sem Similar Nacional\n7 - Estrangeira - Adquirida no Mercado Interno sem Similar Nacional\n8 - Nacional - Conteúdo Importado > 70%",
                "default": "0 - Nacional",
                "insert_after": "cfop_default",
            },
            {
                "fieldname": "icms_cst",
                "label": "ICMS CST",
                "fieldtype": "Select",
                "options": "\n00\n10\n20\n30\n40\n41\n50\n51\n60\n70\n90\nParte",
                "insert_after": "origem_mercadoria",
            },
            {
                "fieldname": "pis_cst",
                "label": "PIS CST",
                "fieldtype": "Select",
                "options": "\n01\n02\n03\n04\n05\n06\n07\n08\n09\n49\n50\n51\n52\n53\n54\n55\n56\n60\n61\n62\n63\n64\n65\n66\n67\n70\n71\n72\n73\n74\n75\n98\n99",
                "insert_after": "icms_cst",
            },
            {
                "fieldname": "cofins_cst",
                "label": "COFINS CST",
                "fieldtype": "Select",
                "options": "\n01\n02\n03\n04\n05\n06\n07\n08\n09\n49\n50\n51\n52\n53\n54\n55\n56\n60\n61\n62\n63\n64\n65\n66\n67\n70\n71\n72\n73\n74\n75\n98\n99",
                "insert_after": "pis_cst",
            },
        ],
        "Customer": [
            {
                "fieldname": "cpf_cnpj",
                "label": "CPF / CNPJ",
                "fieldtype": "Char",
                "insert_after": "customer_name",
                "description": "CPF (11 dígitos) ou CNPJ (14 dígitos)",
            },
            {
                "fieldname": "ie_rg",
                "label": "IE / RG",
                "fieldtype": "Char",
                "insert_after": "cpf_cnpj",
                "description": "Inscrição Estadual (IE) ou RG",
            },
            {
                "fieldname": "contribuinte_icms",
                "label": "Contribuinte ICMS",
                "fieldtype": "Select",
                "options": "\n1 - Contribuinte\n2 - Isento\n9 - Não Contribuinte",
                "default": "9 - Não Contribuinte",
                "insert_after": "ie_rg",
            },
            {
                "fieldname": "suframa",
                "label": "SUFRAMA",
                "fieldtype": "Char",
                "length": 9,
                "insert_after": "contribuinte_icms",
                "description": "Inscrição SUFRAMA (Zona Franca de Manaus)",
            },
        ],
        "Sales Invoice": [
            {
                "fieldname": "nfe_data",
                "label": "NF-e / NFC-e",
                "fieldtype": "Section Break",
                "insert_after": "naming_series",
            },
            {
                "fieldname": "cfop_nfe",
                "label": "CFOP NF-e",
                "fieldtype": "Char",
                "length": 4,
                "insert_after": "nfe_data",
                "description": "CFOP para esta nota fiscal",
            },
            {
                "fieldname": "chave_acesso_nfe",
                "label": "Chave de Acesso NF-e",
                "fieldtype": "Char",
                "length": 44,
                "read_only": 1,
                "insert_after": "cfop_nfe",
            },
            {
                "fieldname": "protocolo_nfe",
                "label": "Protocolo NF-e",
                "fieldtype": "Char",
                "length": 15,
                "read_only": 1,
                "insert_after": "chave_acesso_nfe",
            },
            {
                "fieldname": "xml_nfe",
                "label": "XML NF-e Assinado",
                "fieldtype": "Code",
                "read_only": 1,
                "options": "XML",
                "insert_after": "protocolo_nfe",
            },
            {
                "fieldname": "danfe_pdf",
                "label": "DANFE PDF",
                "fieldtype": "Attach",
                "read_only": 1,
                "insert_after": "xml_nfe",
            },
            {
                "fieldname": "emitir_nfe",
                "label": "",
                "fieldtype": "Section Break",
                "insert_after": "danfe_pdf",
            },
            {
                "fieldname": "emitir_nfe_agora",
                "label": "Emitir NF-e",
                "fieldtype": "Button",
                "insert_after": "emitir_nfe",
                "depends_on": "eval:doc.status=='Submitted' && !doc.chave_acesso_nfe",
            },
        ],
        "POS Invoice": [
            {
                "fieldname": "nfe_data",
                "label": "NFC-e",
                "fieldtype": "Section Break",
                "insert_after": "scan_barcode",
            },
            {
                "fieldname": "cpf_cnpj_consumidor",
                "label": "CPF / CNPJ do Consumidor",
                "fieldtype": "Char",
                "insert_after": "nfe_data",
                "description": "CPF ou CNPJ do consumidor final (opcional)",
            },
            {
                "fieldname": "chave_acesso_nfce",
                "label": "Chave de Acesso NFC-e",
                "fieldtype": "Char",
                "length": 44,
                "read_only": 1,
                "insert_after": "cpf_cnpj_consumidor",
            },
            {
                "fieldname": "protocolo_nfce",
                "label": "Protocolo NFC-e",
                "fieldtype": "Char",
                "length": 15,
                "read_only": 1,
                "insert_after": "chave_acesso_nfce",
            },
            {
                "fieldname": "qr_code_nfce",
                "label": "QR Code NFC-e",
                "fieldtype": "Code",
                "options": "Text",
                "read_only": 1,
                "insert_after": "protocolo_nfce",
            },
            {
                "fieldname": "xml_nfce",
                "label": "XML NFC-e",
                "fieldtype": "Code",
                "read_only": 1,
                "options": "XML",
                "insert_after": "qr_code_nfce",
            },
        ],
    }
    
    create_custom_fields(custom_fields, ignore_validate=True)
    frappe.log_error("Campos fiscais brasileiros criados!", "Brazil Setup")


def setup_print_formats():
    """Configura formatos de impressão brasileiros"""
    print_formats = [
        {
            "name": "Cupom Fiscal 80mm",
            "doc_type": "POS Invoice",
            "format_data": "cupom_fiscal_80mm",
            "css": "",
            "standard": "Brazil",
            "property": "print_format",
        },
    ]
    
    for pf in print_formats:
        if not frappe.db.exists("Print Format", pf["name"]):
            pf_doc = frappe.get_doc({
                "doctype": "Print Format",
                "doc_type": pf["doc_type"],
                "name": pf["name"],
                "print_format_builder": 0,
                "css": pf["css"],
                "standard": "Yes",
            })
            pf_doc.insert(ignore_permissions=True)


def setup_accounts():
    """Configura contas contábeis brasileiras"""
    # O ERPNext já tem o plano de contas brasileiro em:
    # erpnext/accounts/doctype/account/chart_of_accounts/verified/br_planilha_de_contas.json
    # Esse plano é carregado automaticamente ao criar empresa com país Brasil
    pass