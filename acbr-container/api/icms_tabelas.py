"""
Tabelas de Conformidade Fiscal Brasileira

Implementa:
- ICMS por NCM (Nomenclatura Comum Mercosul)
- CST (Código de Situação Tributária) para ICMS, PIS, COFINS
- Regimes tributários (SN, LR, LP)
- Alíquotas padrão conforme legislação
"""

from decimal import Decimal
from typing import Dict, Tuple, Optional
from enum import Enum


# ============================================================================
# REGIMES TRIBUTÁRIOS BRASILEIROS
# ============================================================================

class RegimeTributario(str, Enum):
    """Lei Complementar 123/2006 - Simples Nacional e demais regimes"""
    SIMPLES_NACIONAL = "SN"      # Simples Nacional
    LUCRO_REAL = "LR"             # Lucro Real
    LUCRO_PRESUMIDO = "LP"        # Lucro Presumido


REGIMES_DESCRICAO = {
    "SN": "Simples Nacional",
    "LR": "Lucro Real",
    "LP": "Lucro Presumido",
}


# ============================================================================
# CST ICMS (Código de Situação Tributária ICMS)
# Conforme RICMS-ST (Regulamento do ICMS de cada Estado)
# ============================================================================

CST_ICMS = {
    "00": "Tributada integralmente",
    "10": "Tributada e com cobrança do ICMS por substituição tributária",
    "20": "Tributada com FCP (Fundo de Combate à Pobreza)",
    "30": "Isenta",
    "40": "Não tributada",
    "41": "Não tributada (saída)",
    "50": "Suspensão",
    "51": "Diferimento",
    "60": "ICMS cobrado anteriormente por ST",
    "70": "Com redução de base de cálculo",
    "90": "Outras operações",
}


# ============================================================================
# CST PIS (Código de Situação Tributária - Contribuição para PIS)
# Lei 10.637/2002
# ============================================================================

CST_PIS = {
    "01": "Operação tributável com alíquota básica",
    "02": "Operação tributável com alíquota diferenciada",
    "03": "Operação tributável com alíquota por unidade de medida de produto",
    "04": "Operação tributável monofásica - revenda por alíquota básica",
    "05": "Operação tributável por substituição tributária",
    "06": "Operação tributável a alíquota zero",
    "07": "Operação isenta da contribuição",
    "08": "Operação sem incidência da contribuição",
    "09": "Operação com suspensão da contribuição",
    "49": "Outras operações de saída",
    "50": "Operação com direito a crédito - vinculada exclusivamente a receita tributada no mercado interno",
    "51": "Operação com direito a crédito - vinculada exclusivamente a receita não tributada no mercado interno",
    "52": "Operação com direito a crédito - vinculada exclusivamente a receita de exportação",
    "53": "Operação com direito a crédito - vinculada a receitas tributadas e não tributadas no mercado interno",
    "54": "Operação com direito a crédito - vinculada a receitas tributadas no mercado interno e de exportação",
    "55": "Operação com direito a crédito - vinculada a receitas não tributadas no mercado interno e de exportação",
    "56": "Operação com direito a crédito - vinculada a receitas tributadas e não tributadas no mercado interno, e de exportação",
    "60": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita tributada",
    "61": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita não tributada",
    "62": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita de exportação",
    "63": "Crédito presumido - operação de aquisição vinculada a recetas tributadas e não tributadas",
    "64": "Crédito presumido - operação de aquisição vinculada a recetas tributadas e de exportação",
    "65": "Crédito presumido - operação de aquisição vinculada a recetas não tributadas e de exportação",
    "66": "Crédito presumido - operação de aquisição vinculada a recetas tributadas, não tributadas e de exportação",
    "67": "Crédito presumido - outras operações",
    "70": "Operação de aquisição sem direito a crédito",
    "71": "Operação de aquisição com isenção",
    "72": "Operação de aquisição com suspensão",
    "73": "Operação de aquisição com diferimento",
    "74": "Operação de aquisição com direito a crédito - vinculada exclusivamente a receita não tributada no mercado interno",
    "75": "Operação de aquisição com direito a crédito - vinculada exclusivamente a receita de exportação",
    "98": "Outras operações de entrada",
    "99": "Outras operações",
}


# ============================================================================
# CST COFINS (Código de Situação Tributária - Contribuição Social sobre Faturamento)
# Lei 10.833/2003
# ============================================================================

CST_COFINS = {
    "01": "Operação tributável com alíquota básica",
    "02": "Operação tributável com alíquota diferenciada",
    "03": "Operação tributável com alíquota por unidade de medida de produto",
    "04": "Operação tributável monofásica - revenda por alíquota básica",
    "05": "Operação tributável por substituição tributária",
    "06": "Operação tributável a alíquota zero",
    "07": "Operação isenta da contribuição",
    "08": "Operação sem incidência da contribuição",
    "09": "Operação com suspensão da contribuição",
    "49": "Outras operações de saída",
    "50": "Operação com direito a crédito - vinculada exclusivamente a receita tributada no mercado interno",
    "51": "Operação com direito a crédito - vinculada exclusivamente a receita não tributada no mercado interno",
    "52": "Operação com direito a crédito - vinculada exclusivamente a receita de exportação",
    "53": "Operação com direito a crédito - vinculada a receitas tributadas e não tributadas no mercado interno",
    "54": "Operação com direito a crédito - vinculada a receitas tributadas no mercado interno e de exportação",
    "55": "Operação com direito a crédito - vinculada a receitas não tributadas no mercado interno e de exportação",
    "56": "Operação com direito a crédito - vinculada a receitas tributadas e não tributadas no mercado interno, e de exportação",
    "60": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita tributada",
    "61": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita não tributada",
    "62": "Crédito presumido - operação de aquisição vinculada exclusivamente a receita de exportação",
    "63": "Crédito presumido - operação de aquisição vinculada a recetas tributadas e não tributadas",
    "64": "Crédito presumido - operação de aquisição vinculada a recetas tributadas e de exportação",
    "65": "Crédito presumido - operação de aquisição vinculada a recetas não tributadas e de exportação",
    "66": "Crédito presumido - operação de aquisição vinculada a recetas tributadas, não tributadas e de exportação",
    "67": "Crédito presumido - outras operações",
    "70": "Operação de aquisição sem direito a crédito",
    "71": "Operação de aquisição com isenção",
    "72": "Operação de aquisição com suspensão",
    "73": "Operação de aquisição com diferimento",
    "74": "Operação de aquisição com direito a crédito - vinculada exclusivamente a receita não tributada no mercado interno",
    "75": "Operação de aquisição com direito a crédito - vinculada exclusivamente a receita de exportação",
    "98": "Outras operações de entrada",
    "99": "Outras operações",
}


# ============================================================================
# ALÍQUOTAS PADRÃO (Lei Complementar 123/2006 + Lei 10.637/2002 + Lei 10.833/2003)
# ============================================================================

ALIQUOTA_PIS_PADRAO = Decimal("7.65")      # 7,65% - aliquota padrão cumulativa
ALIQUOTA_COFINS_PADRAO = Decimal("7.65")   # 7,65% - aliquota padrão cumulativa


# ============================================================================
# ICMS POR NCM E UF
# Tabela dinâmica: chave (NCM, UF) → alíquota ICMS
# Exemplo com produtos comuns
# ============================================================================

ICMS_ALIQUOTA_POR_NCM_UF: Dict[Tuple[str, str], Decimal] = {
    # Alimentos (geralmente 12% em maioria dos estados)
    ("02012100", "AC"): Decimal("17.00"),  # Carne bovina - Acre
    ("02012100", "AL"): Decimal("17.00"),  # Carne bovina - Alagoas
    ("02012100", "AP"): Decimal("17.00"),  # Carne bovina - Amapá
    ("02012100", "AM"): Decimal("17.00"),  # Carne bovina - Amazonas
    ("02012100", "BA"): Decimal("17.00"),  # Carne bovina - Bahia
    ("02012100", "CE"): Decimal("17.00"),  # Carne bovina - Ceará
    ("02012100", "DF"): Decimal("17.00"),  # Carne bovina - Distrito Federal
    ("02012100", "ES"): Decimal("17.00"),  # Carne bovina - Espírito Santo
    ("02012100", "GO"): Decimal("17.00"),  # Carne bovina - Goiás
    ("02012100", "MA"): Decimal("17.00"),  # Carne bovina - Maranhão
    ("02012100", "MT"): Decimal("17.00"),  # Carne bovina - Mato Grosso
    ("02012100", "MS"): Decimal("17.00"),  # Carne bovina - Mato Grosso do Sul
    ("02012100", "MG"): Decimal("12.00"),  # Carne bovina - Minas Gerais
    ("02012100", "PA"): Decimal("17.00"),  # Carne bovina - Pará
    ("02012100", "PB"): Decimal("17.00"),  # Carne bovina - Paraíba
    ("02012100", "PR"): Decimal("12.00"),  # Carne bovina - Paraná
    ("02012100", "PE"): Decimal("17.00"),  # Carne bovina - Pernambuco
    ("02012100", "PI"): Decimal("17.00"),  # Carne bovina - Piauí
    ("02012100", "RJ"): Decimal("20.00"),  # Carne bovina - Rio de Janeiro
    ("02012100", "RN"): Decimal("17.00"),  # Carne bovina - Rio Grande do Norte
    ("02012100", "RS"): Decimal("12.00"),  # Carne bovina - Rio Grande do Sul
    ("02012100", "RO"): Decimal("17.00"),  # Carne bovina - Rondônia
    ("02012100", "RR"): Decimal("17.00"),  # Carne bovina - Roraima
    ("02012100", "SC"): Decimal("12.00"),  # Carne bovina - Santa Catarina
    ("02012100", "SP"): Decimal("12.00"),  # Carne bovina - São Paulo
    ("02012100", "SE"): Decimal("17.00"),  # Carne bovina - Sergipe
    ("02012100", "TO"): Decimal("17.00"),  # Carne bovina - Tocantins

    # Carne de porco
    ("02011000", "SP"): Decimal("12.00"),
    ("02011000", "MG"): Decimal("12.00"),
    ("02011000", "RJ"): Decimal("20.00"),
    ("02011000", "RS"): Decimal("12.00"),
    ("02011000", "SC"): Decimal("12.00"),

    # Batata (alimento)
    ("07011000", "SP"): Decimal("12.00"),
    ("07011000", "MG"): Decimal("12.00"),
    ("07011000", "RS"): Decimal("12.00"),

    # Equipamentos (geralmente 18%)
    ("84431000", "SP"): Decimal("18.00"),
    ("84431000", "MG"): Decimal("18.00"),
    ("84431000", "RJ"): Decimal("20.00"),
    ("84431000", "RS"): Decimal("18.00"),

    # Bebidas (cerveja, refrigerante)
    ("22030000", "SP"): Decimal("12.00"),
    ("22030000", "MG"): Decimal("12.00"),
    ("22030000", "RJ"): Decimal("20.00"),

    # Cosméticos
    ("33049900", "SP"): Decimal("18.00"),
    ("33049900", "MG"): Decimal("18.00"),
    ("33049900", "RJ"): Decimal("20.00"),

    # Eletrônicos
    ("85171190", "SP"): Decimal("18.00"),
    ("85171190", "MG"): Decimal("18.00"),
    ("85171190", "RJ"): Decimal("20.00"),
}


def obter_aliquota_icms(ncm: str, uf: str) -> Decimal:
    """
    Obtém alíquota ICMS para um NCM e UF específicos

    Args:
        ncm: Código NCM (8 dígitos)
        uf: Estado (2 dígitos)

    Returns:
        Alíquota ICMS em Decimal, ou 18% (padrão) se não encontrada
    """
    chave = (ncm, uf)
    return ICMS_ALIQUOTA_POR_NCM_UF.get(chave, Decimal("18.00"))


def validar_cst_icms(cst: str) -> bool:
    """Valida se CST ICMS é válido"""
    return cst in CST_ICMS


def validar_cst_pis(cst: str) -> bool:
    """Valida se CST PIS é válido"""
    return cst in CST_PIS


def validar_cst_cofins(cst: str) -> bool:
    """Valida se CST COFINS é válido"""
    return cst in CST_COFINS


def validar_regime_tributario(regime: str) -> bool:
    """Valida se regime tributário é válido"""
    return regime in [r.value for r in RegimeTributario]


def obter_descricao_regime(regime: str) -> Optional[str]:
    """Retorna descrição legível do regime"""
    return REGIMES_DESCRICAO.get(regime)


def obter_descricao_cst_icms(cst: str) -> Optional[str]:
    """Retorna descrição legível do CST ICMS"""
    return CST_ICMS.get(cst)


def obter_descricao_cst_pis(cst: str) -> Optional[str]:
    """Retorna descrição legível do CST PIS"""
    return CST_PIS.get(cst)


def obter_descricao_cst_cofins(cst: str) -> Optional[str]:
    """Retorna descrição legível do CST COFINS"""
    return CST_COFINS.get(cst)
