"""
Formatadores de documentos brasileiros
"""


def formatar_cpf(cpf: str) -> str:
    """Formata CPF: XXX.XXX.XXX-XX"""
    cpf = cpf.zfill(11)
    return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ: XX.XXX.XXX/XXXX-XX"""
    cnpj = cnpj.zfill(14)
    return f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}"


def formatar_cep(cep: str) -> str:
    """Formata CEP: XXXXX-XXX"""
    cep = cep.zfill(8)
    return f"{cep[:5]}-{cep[5:]}"


def formatar_telefone(telefone: str) -> str:
    """Formata telefone: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"""
    tel = telefone.replace("(", "").replace(")", "").replace("-", "").replace(" ", "")
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    elif len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    return telefone