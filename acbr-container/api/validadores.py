"""
Validação de CPF e CNPJ
Implementação pura em Python (não requer ACBrLib)
"""

import re


def validar_cpf(cpf: str) -> tuple[bool, str]:
    """
    Valida um CPF (11 dígitos)
    Retorna (True, "CPF válido") ou (False, "motivo")
    """
    # Limpar string
    cpf = re.sub(r"\D", "", cpf)

    if len(cpf) != 11:
        return False, "CPF deve ter 11 dígitos"

    if cpf == cpf[0] * 11:
        return False, "CPF inválido: dígitos repetidos"

    # Calcular 1º dígito verificador
    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    resto = (soma * 10) % 11
    dig1 = 0 if resto > 9 else resto

    if int(cpf[9]) != dig1:
        return False, f"1º dígito verificador inválido (esperado {dig1}, obtido {cpf[9]})"

    # Calcular 2º dígito verificador
    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    resto = (soma * 10) % 11
    dig2 = 0 if resto > 9 else resto

    if int(cpf[10]) != dig2:
        return False, f"2º dígito verificador inválido (esperado {dig2}, obtido {cpf[10]})"

    return True, "CPF válido"


def validar_cnpj(cnpj: str) -> tuple[bool, str]:
    """
    Valida um CNPJ (14 dígitos)
    Retorna (True, "CNPJ válido") ou (False, "motivo")
    """
    # Limpar string
    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        return False, "CNPJ deve ter 14 dígitos"

    if cnpj == cnpj[0] * 14:
        return False, "CNPJ inválido: dígitos repetidos"

    # Calcular 1º dígito verificador
    pesos1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos1[i] for i in range(12))
    resto = soma % 11
    dig1 = 0 if resto < 2 else 11 - resto

    if int(cnpj[12]) != dig1:
        return False, f"1º dígito verificador inválido (esperado {dig1}, obtido {cnpj[12]})"

    # Calcular 2º dígito verificador
    pesos2 = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    soma = sum(int(cnpj[i]) * pesos2[i] for i in range(13))
    resto = soma % 11
    dig2 = 0 if resto < 2 else 11 - resto

    if int(cnpj[13]) != dig2:
        return False, f"2º dígito verificador inválido (esperado {dig2}, obtido {cnpj[13]})"

    return True, "CNPJ válido"