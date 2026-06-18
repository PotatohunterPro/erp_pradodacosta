"""
Formatadores de documentos brasileiros (cópia local)
"""


def formatar_cpf(cpf: str) -> str:
    """Formata CPF: XXX.XXX.XXX-XX"""
    nums = "".join(c for c in cpf if c.isdigit()).zfill(11)
    return f"{nums[:3]}.{nums[3:6]}.{nums[6:9]}-{nums[9:]}"


def formatar_cnpj(cnpj: str) -> str:
    """Formata CNPJ: XX.XXX.XXX/XXXX-XX"""
    nums = "".join(c for c in cnpj if c.isdigit()).zfill(14)
    return f"{nums[:2]}.{nums[2:5]}.{nums[5:8]}/{nums[8:12]}-{nums[12:]}"


def formatar_cep(cep: str) -> str:
    """Formata CEP: XXXXX-XXX"""
    nums = "".join(c for c in cep if c.isdigit()).zfill(8)
    return f"{nums[:5]}-{nums[5:]}"


def formatar_telefone(telefone: str) -> str:
    """Formata telefone brasileiro: (XX) XXXXX-XXXX"""
    tel = "".join(c for c in telefone if c.isdigit())
    if len(tel) == 11:
        return f"({tel[:2]}) {tel[2:7]}-{tel[7:]}"
    elif len(tel) == 10:
        return f"({tel[:2]}) {tel[2:6]}-{tel[6:]}"
    return telefone


def formatar_valor_monetario(valor: float) -> str:
    """Formata valor em R$: 1.234,56"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def valor_por_extenso(valor: float) -> str:
    """
    Converte valor para extenso (usado em cheques e DANFE)
    Exemplo: R$ 1.234,56 -> "mil duzentos e trinta e quatro reais e cinquenta e seis centavos"
    
    TODO: Implementar função completa de valor por extenso
    """
    if valor == 0:
        return "zero reais"
    
    reais = int(valor)
    centavos = int(round((valor - reais) * 100))
    
    extenso_reais = _numero_por_extenso(reais, "real", "reais")
    extenso_centavos = _numero_por_extenso(centavos, "centavo", "centavos")
    
    if centavos == 0:
        return extenso_reais
    if reais == 0:
        return extenso_centavos
    
    return f"{extenso_reais} e {extenso_centavos}"


def _numero_por_extenso(num: int, singular: str, plural: str) -> str:
    """
    Converte número inteiro para extenso (implementação básica)
    TODO: Expandir para valores maiores que 999 bilhões
    """
    unidades = ["", "um", "dois", "três", "quatro", "cinco", "seis", "sete", "oito", "nove"]
    especiais = ["dez", "onze", "doze", "treze", "quatorze", "quinze", "dezesseis", 
                 "dezessete", "dezoito", "dezenove"]
    dezenas = ["", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", 
               "setenta", "oitenta", "noventa"]
    centenas = ["", "cento", "duzentos", "trezentos", "quatrocentos", "quinhentos",
                "seiscentos", "setecentos", "oitocentos", "novecentos"]
    
    if num == 0:
        return f"zero {plural}"
    if num == 1:
        return f"{singular}"
    
    palavras = []
    
    # Bilhões
    if num >= 1_000_000_000:
        b = num // 1_000_000_000
        palavras.append(_numero_por_extenso(b, "bilhão", "bilhões"))
        num %= 1_000_000_000
    
    # Milhões
    if num >= 1_000_000:
        m = num // 1_000_000
        palavras.append(_numero_por_extenso(m, "milhão", "milhões"))
        num %= 1_000_000
    
    # Milhares
    if num >= 1_000:
        k = num // 1_000
        if k == 1:
            palavras.append("mil")
        else:
            palavras.append(f"{_numero_por_extenso(k, '', '')} mil")
        num %= 1_000
    
    # Centenas
    if num >= 100:
        cent = num // 100
        if cent == 1 and num % 100 == 0:
            palavras.append("cem")
        else:
            palavras.append(centenas[cent])
        num %= 100
    
    # Dezenas e unidades
    if num >= 20:
        palavras.append(dezenas[num // 10])
        num %= 10
    elif 10 <= num < 20:
        palavras.append(especiais[num - 10])
        num = 0
    
    if num > 0:
        palavras.append(unidades[num])
    
    texto = " e ".join(palavras)
    if num == 0 and not any(c in texto for c in "e"):
        pass  # already handled
    
    return f"{texto} {singular if num <= 1 and texto == 'um' else plural}"