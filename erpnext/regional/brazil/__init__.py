# Módulo de Regionalização Brasil para ERPNext
"""
Módulo fiscal brasileiro para ERPNext.

Este módulo implementa as adequações necessárias para o cenário fiscal brasileiro:
- NF-e (Nota Fiscal Eletrônica) / NFC-e (Cupom Fiscal Eletrônico)
- CFOP, NCM, CEST, IBPT
- Validação de CPF/CNPJ
- Layout de cupom fiscal térmico (80mm)
- Integração com SEFAZ via ACBrLib
- DANFE, boletos e documentos fiscais

Este módulo é ativado através do domínio "Brazil" nas configurações do ERPNext.
"""

__version__ = "1.0.0"

from erpnext.regional.brazil.setup import setup_brazil, after_install