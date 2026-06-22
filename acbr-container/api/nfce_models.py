"""
Modelos Pydantic para NFC-e

Define estrutura e validação de dados para geração de NFC-e
"""

from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional
from decimal import Decimal


class ProdutoNfce(BaseModel):
    """Produto em uma NFC-e"""

    ncm: str = Field(..., description="Nomenclatura Comum do Mercosul (8 dígitos)")
    cfop: str = Field(..., description="Código Fiscal Operações (4 dígitos)")
    descricao: str = Field(..., min_length=1, max_length=120)
    quantidade: float = Field(..., gt=0, description="Quantidade do produto")
    valor_unitario: Decimal = Field(..., ge=0, description="Valor unitário em reais")
    aliquota_icms: float = Field(default=18.0, ge=0, le=100)
    aliquota_pis: float = Field(default=7.65, ge=0, le=100)
    aliquota_cofins: float = Field(default=7.65, ge=0, le=100)
    cst_icms: str = Field(default="00", description="Código de Situação Tributária ICMS")
    cst_pis: str = Field(default="01", description="Código de Situação Tributária PIS")
    cst_cofins: str = Field(default="01", description="Código de Situação Tributária COFINS")
    origem: str = Field(default="0", description="Origem da mercadoria (0-8)")

    @field_validator('ncm')
    @classmethod
    def validar_ncm(cls, v):
        """NCM deve ter exatamente 8 dígitos"""
        if not v.isdigit() or len(v) != 8:
            raise ValueError('NCM deve ter 8 dígitos (ex: 84431000)')
        return v

    @field_validator('cfop')
    @classmethod
    def validar_cfop(cls, v):
        """CFOP deve ter exatamente 4 dígitos"""
        if not v.isdigit() or len(v) != 4:
            raise ValueError('CFOP deve ter 4 dígitos (ex: 5102)')
        return v

    @field_validator('origem')
    @classmethod
    def validar_origem(cls, v):
        """Origem deve estar entre 0 e 8"""
        if not v.isdigit() or int(v) > 8:
            raise ValueError('Origem deve estar entre 0 e 8')
        return v

    def valor_total(self) -> Decimal:
        """Calcula valor total do produto"""
        return Decimal(str(self.quantidade)) * self.valor_unitario


class ConsumidorNfce(BaseModel):
    """Consumidor da NFC-e (opcional)"""

    cpf_cnpj: str = Field(..., description="CPF (11 dígitos) ou CNPJ (14 dígitos)")
    nome: Optional[str] = Field(None, max_length=60)

    @field_validator('cpf_cnpj')
    @classmethod
    def validar_cpf_cnpj(cls, v):
        """Valida se é CPF ou CNPJ"""
        if not v.isdigit():
            raise ValueError('CPF/CNPJ deve conter apenas dígitos')

        if len(v) == 11:
            # CPF: simples validação de tamanho
            return v
        elif len(v) == 14:
            # CNPJ: simples validação de tamanho
            return v
        else:
            raise ValueError('CPF deve ter 11 dígitos, CNPJ deve ter 14')

        return v


class EmitenteNfce(BaseModel):
    """Dados do Emitente da NFC-e"""

    cnpj: str = Field(..., description="CNPJ do emitente (14 dígitos)")
    ie: str = Field(..., description="Inscrição Estadual (ICMS)")
    nome_fantasia: str = Field(..., max_length=60)
    razao_social: str = Field(..., max_length=60)
    endereco: str = Field(..., max_length=120)
    numero: str = Field(..., max_length=20)
    complemento: Optional[str] = Field(None, max_length=60)
    bairro: str = Field(..., max_length=60)
    municipio: str = Field(..., max_length=60)
    uf: str = Field(..., min_length=2, max_length=2)
    cep: str = Field(..., description="CEP (8 dígitos)")
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[str] = Field(None, max_length=120)

    @field_validator('cnpj')
    @classmethod
    def validar_cnpj(cls, v):
        """Valida CNPJ (14 dígitos)"""
        if not v.isdigit() or len(v) != 14:
            raise ValueError('CNPJ deve ter 14 dígitos')
        return v

    @field_validator('cep')
    @classmethod
    def validar_cep(cls, v):
        """Valida CEP (8 dígitos)"""
        if not v.isdigit() or len(v) != 8:
            raise ValueError('CEP deve ter 8 dígitos')
        return v

    @field_validator('uf')
    @classmethod
    def validar_uf(cls, v):
        """Valida se UF é válida"""
        ufs_validas = [
            'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
            'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
            'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
        ]
        if v.upper() not in ufs_validas:
            raise ValueError(f'UF inválida: {v}')
        return v.upper()


class NfcePayload(BaseModel):
    """Payload para geração de NFC-e"""

    emitente: EmitenteNfce
    produtos: list[ProdutoNfce] = Field(..., min_length=1)
    consumidor: Optional[ConsumidorNfce] = None
    observacao: Optional[str] = Field(None, max_length=500)

    # Dados adicionais
    numero_nfce: Optional[int] = Field(default=1, description="Número da NFC-e (sequencial)")
    serie_nfce: int = Field(default=65, description="Série da NFC-e (sempre 65 para NFC-e)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "emitente": {
                    "cnpj": "06117114000172",
                    "ie": "123456789012",
                    "nome_fantasia": "Loja Exemplo",
                    "razao_social": "Loja Exemplo LTDA",
                    "endereco": "Rua das Flores",
                    "numero": "100",
                    "bairro": "Centro",
                    "municipio": "São Paulo",
                    "uf": "SP",
                    "cep": "01234567",
                    "email": "contato@loja.com"
                },
                "produtos": [
                    {
                        "ncm": "84431000",
                        "cfop": "5102",
                        "descricao": "Produto Exemplo",
                        "quantidade": 1,
                        "valor_unitario": "100.00",
                        "aliquota_icms": 18.0
                    }
                ],
                "consumidor": {
                    "cpf_cnpj": "12345678901234"
                }
            }
        }
    )

    def valor_total_produtos(self) -> Decimal:
        """Calcula valor total de todos os produtos"""
        return sum(p.valor_total() for p in self.produtos)

    def valor_total_icms(self) -> Decimal:
        """Calcula ICMS total"""
        total = Decimal('0')
        for p in self.produtos:
            valor_produto = p.valor_total()
            icms = valor_produto * Decimal(str(p.aliquota_icms / 100))
            total += icms
        return total

    def valor_total_pis(self) -> Decimal:
        """Calcula PIS total"""
        total = Decimal('0')
        for p in self.produtos:
            valor_produto = p.valor_total()
            pis = valor_produto * Decimal(str(p.aliquota_pis / 100))
            total += pis
        return total

    def valor_total_cofins(self) -> Decimal:
        """Calcula COFINS total"""
        total = Decimal('0')
        for p in self.produtos:
            valor_produto = p.valor_total()
            cofins = valor_produto * Decimal(str(p.aliquota_cofins / 100))
            total += cofins
        return total
