"""
Testes para Conformidade Fiscal nos Modelos NFC-e

Valida:
- Validação de CST ICMS, PIS, COFINS na criação de produtos
- Validação de Regime Tributário no emitente
- Cálculos dinâmicos de ICMS conforme NCM/UF
"""

import pytest
from decimal import Decimal
from api.nfce_models import (
    ProdutoNfce,
    EmitenteNfce,
    NfcePayload,
)


class TestCstIcmsValidacao:
    """Testes para validação de CST ICMS em produtos"""

    def test_produto_com_cst_icms_00(self):
        """Produto com CST ICMS 00 deve ser válido"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto com CST 00",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            cst_icms="00",
        )
        assert produto.cst_icms == "00"

    def test_produto_com_cst_icms_40(self):
        """Produto com CST ICMS 40 (Não tributada) deve ser válido"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto não tributado",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            cst_icms="40",
        )
        assert produto.cst_icms == "40"

    def test_produto_com_cst_icms_invalido(self):
        """Produto com CST ICMS inválido deve ser rejeitado"""
        with pytest.raises(ValueError, match="CST ICMS inválido"):
            ProdutoNfce(
                ncm="84431000",
                cfop="5102",
                descricao="Produto inválido",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
                cst_icms="99",
            )

    def test_produto_cst_icms_default_00(self):
        """CST ICMS padrão deve ser 00"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
        )
        assert produto.cst_icms == "00"


class TestCstPisValidacao:
    """Testes para validação de CST PIS em produtos"""

    def test_produto_com_cst_pis_01(self):
        """Produto com CST PIS 01 deve ser válido"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            cst_pis="01",
        )
        assert produto.cst_pis == "01"

    def test_produto_com_cst_pis_07(self):
        """Produto com CST PIS 07 (Isenta) deve ser válido"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto isento",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            cst_pis="07",
        )
        assert produto.cst_pis == "07"

    def test_produto_com_cst_pis_invalido(self):
        """Produto com CST PIS inválido deve ser rejeitado"""
        with pytest.raises(ValueError, match="CST PIS inválido"):
            ProdutoNfce(
                ncm="84431000",
                cfop="5102",
                descricao="Produto inválido",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
                cst_pis="11",
            )


class TestCstCofinsValidacao:
    """Testes para validação de CST COFINS em produtos"""

    def test_produto_com_cst_cofins_01(self):
        """Produto com CST COFINS 01 deve ser válido"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            cst_cofins="01",
        )
        assert produto.cst_cofins == "01"

    def test_produto_com_cst_cofins_invalido(self):
        """Produto com CST COFINS inválido deve ser rejeitado"""
        with pytest.raises(ValueError, match="CST COFINS inválido"):
            ProdutoNfce(
                ncm="84431000",
                cfop="5102",
                descricao="Produto inválido",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
                cst_cofins="11",
            )


class TestRegimeTributarioValidacao:
    """Testes para validação de Regime Tributário no emitente"""

    def test_emitente_regime_simples_nacional(self):
        """Emitente com regime SN deve ser válido"""
        emitente = EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja SN",
            razao_social="Loja SN LTDA",
            endereco="Rua Teste",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="SP",
            cep="01234567",
            regime_tributario="SN",
        )
        assert emitente.regime_tributario == "SN"

    def test_emitente_regime_lucro_real(self):
        """Emitente com regime LR deve ser válido"""
        emitente = EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja LR",
            razao_social="Loja LR LTDA",
            endereco="Rua Teste",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="SP",
            cep="01234567",
            regime_tributario="LR",
        )
        assert emitente.regime_tributario == "LR"

    def test_emitente_regime_invalido(self):
        """Emitente com regime inválido deve ser rejeitado"""
        with pytest.raises(ValueError, match="Regime tributário inválido"):
            EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Loja Inválida",
                razao_social="Loja Inválida LTDA",
                endereco="Rua Teste",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
                regime_tributario="XX",
            )

    def test_emitente_regime_default_sn(self):
        """Regime padrão deve ser SN (Simples Nacional)"""
        emitente = EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja",
            razao_social="Loja LTDA",
            endereco="Rua Teste",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="SP",
            cep="01234567",
        )
        assert emitente.regime_tributario == "SN"


class TestIcmsDinamico:
    """Testes para cálculo dinâmico de ICMS conforme NCM/UF"""

    def test_payload_obter_aliquota_icms_sp(self):
        """Payload deve retornar alíquota ICMS correta para NCM em SP"""
        payload = NfcePayload(
            emitente=EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Açougue SP",
                razao_social="Açougue SP LTDA",
                endereco="Rua Teste",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="02012100",  # Carne bovina
                    cfop="5102",
                    descricao="Carne Vermelha",
                    quantidade=1.0,
                    valor_unitario=Decimal("100.00"),
                )
            ],
        )
        aliquota = payload.obter_aliquota_icms_por_ncm("02012100")
        assert aliquota == Decimal("12.00")

    def test_payload_obter_aliquota_icms_rj(self):
        """Payload deve retornar alíquota ICMS correta para NCM no RJ"""
        payload = NfcePayload(
            emitente=EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Açougue RJ",
                razao_social="Açougue RJ LTDA",
                endereco="Rua Teste",
                numero="100",
                bairro="Centro",
                municipio="Rio de Janeiro",
                uf="RJ",
                cep="01234567",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="02012100",  # Carne bovina
                    cfop="5102",
                    descricao="Carne Vermelha",
                    quantidade=1.0,
                    valor_unitario=Decimal("100.00"),
                )
            ],
        )
        aliquota = payload.obter_aliquota_icms_por_ncm("02012100")
        assert aliquota == Decimal("20.00")

    def test_payload_regime_tributario(self):
        """Payload deve retornar regime do emitente"""
        payload = NfcePayload(
            emitente=EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Loja",
                razao_social="Loja LTDA",
                endereco="Rua Teste",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
                regime_tributario="LR",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="84431000",
                    cfop="5102",
                    descricao="Produto",
                    quantidade=1.0,
                    valor_unitario=Decimal("100.00"),
                )
            ],
        )
        assert payload.regime_tributario() == "LR"


class TestCenarioCompleto:
    """Testes de cenários completos com conformidade fiscal"""

    def test_nfce_completa_com_conformidade(self):
        """NFC-e completa com todos os campos de conformidade"""
        payload = NfcePayload(
            emitente=EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Açougue Central",
                razao_social="Açougue Central LTDA",
                endereco="Rua Principal",
                numero="500",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
                regime_tributario="SN",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="02012100",  # Carne bovina
                    cfop="5102",
                    descricao="Carne Vermelha Premium",
                    quantidade=2.5,
                    valor_unitario=Decimal("45.90"),
                    aliquota_icms=12.0,
                    aliquota_pis=7.65,
                    aliquota_cofins=7.65,
                    cst_icms="00",
                    cst_pis="01",
                    cst_cofins="01",
                    origem="0",
                ),
                ProdutoNfce(
                    ncm="02011000",  # Carne de porco
                    cfop="5102",
                    descricao="Carne de Porco",
                    quantidade=1.0,
                    valor_unitario=Decimal("25.50"),
                    aliquota_icms=12.0,
                    aliquota_pis=7.65,
                    aliquota_cofins=7.65,
                    cst_icms="00",
                    cst_pis="01",
                    cst_cofins="01",
                    origem="0",
                ),
            ],
        )

        assert payload.emitente.regime_tributario == "SN"
        assert len(payload.produtos) == 2
        assert payload.valor_total_produtos() == Decimal("140.25")
        assert payload.obter_aliquota_icms_por_ncm("02012100") == Decimal("12.00")

    def test_nfce_regime_lucro_real(self):
        """NFC-e com regime Lucro Real"""
        payload = NfcePayload(
            emitente=EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Distribuidora LR",
                razao_social="Distribuidora LR LTDA",
                endereco="Rua Comercial",
                numero="200",
                bairro="Industrial",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
                regime_tributario="LR",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="84431000",
                    cfop="5102",
                    descricao="Equipamento",
                    quantidade=1.0,
                    valor_unitario=Decimal("1000.00"),
                    aliquota_icms=18.0,
                    cst_icms="00",
                    cst_pis="01",
                    cst_cofins="01",
                )
            ],
        )

        assert payload.regime_tributario() == "LR"
        assert payload.valor_total_produtos() == Decimal("1000.00")
        assert payload.valor_total_icms() == Decimal("180.00")
