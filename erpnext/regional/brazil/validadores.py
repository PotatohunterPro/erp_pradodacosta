"""
Validadores de documentos brasileiros (cópia local para fallback)
Estas funções também existem no container ACBr, mas mantemos cópia local
para operação offline e validação rápida no cliente
"""

import re


def validar_cpf(cpf: str) -> tuple[bool, str]:
    """Valida CPF (11 dígitos)"""
    cpf = re.sub(r"\D", "", cpf)
    
    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"
    if cpf == cpf[0] * 11:
        return False, "CPF inválido: todos os dígitos iguais"
    
    # 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    dig1 = (soma * 10) % 11
    dig1 = 0 if dig1 > 9 else dig1
    
    if int(cpf[9]) != dig1:
        return False, f"1º dígito verificador inválido"
    
    # 2º dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    dig2 = (soma * 10) % 11
    dig2 = 0 if dig2 > 9 else dig2
    
    if int(cpf[10]) != dig2:
        return False, f"2º dígito verificador inválido"
    
    return True, "CPF válido"


def validar_cnpj(cnpj: str) -> tuple[bool, str]:
    """Valida CNPJ (14 dígitos)"""
    cnpj = re.sub(r"\D", "", cnpj)
    
    if len(cnpj) != 14:
        return False, "CNPJ deve ter 14 dígitos"
    if cnpj == cnpj[0] * 14:
        return False, "CNPJ inválido: todos os dígitos iguais"
    
    # 1º dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    dig1 = 0 if soma % 11 < 2 else 11 - (soma % 11)
    
    if int(cnpj[12]) != dig1:
        return False, f"1º dígito verificador inválido"
    
    # 2º dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    dig2 = 0 if soma % 11 < 2 else 11 - (soma % 11)
    
    if int(cnpj[13]) != dig2:
        return False, f"2º dígito verificador inválido"
    
    return True, "CNPJ válido"


def validar_ie(ie: str, uf: str = "") -> tuple[bool, str]:
    """
    Valida Inscrição Estadual (IE)
    TODO: Implementar validação específica por UF
    """
    if not ie:
        return False, "IE não informada"
    ie = re.sub(r"\D", "", ie)
    if len(ie) < 8 or len(ie) > 14:
        return False, f"IE deve ter entre 8 e 14 dígitos (fornecido: {len(ie)})"
    return True, "IE válida (pendente validação por UF)"


def validar_cep(cep: str) -> tuple[bool, str]:
    """Valida CEP (8 dígitos)"""
    cep = re.sub(r"\D", "", cep)
    if len(cep) != 8:
        return False, "CEP deve ter 8 dígitos"
    return True, "CEP válido"