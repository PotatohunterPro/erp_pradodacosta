"""
Testes para Geração de NFC-e

Segue TDD First: testes primeiro, implementação depois
"""

import pytest
from decimal import Decimal
from api.nfce_models import (
    ProdutoNfce,
    ConsumidorNfce,
    EmitenteNfce,
    NfcePayload
)


class TestProdutoNfce:
    """Testes para modelo de Produto"""

    def test_produto_valido(self):
        """Deve aceitar produto com dados válidos"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
        )
        assert produto.ncm == "84431000"
        assert produto.cfop == "5102"

    def test_ncm_invalido_7_digitos(self):
        """Deve rejeitar NCM com 7 dígitos"""
        with pytest.raises(ValueError, match="8 dígitos"):
            ProdutoNfce(
                ncm="8443100",  # Só 7 dígitos
                cfop="5102",
                descricao="Produto Teste",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
            )

    def test_ncm_invalido_nao_numerico(self):
        """Deve rejeitar NCM não numérico"""
        with pytest.raises(ValueError, match="8 dígitos"):
            ProdutoNfce(
                ncm="8443100A",
                cfop="5102",
                descricao="Produto Teste",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
            )

    def test_cfop_invalido_3_digitos(self):
        """Deve rejeitar CFOP com 3 dígitos"""
        with pytest.raises(ValueError, match="4 dígitos"):
            ProdutoNfce(
                ncm="84431000",
                cfop="510",  # Só 3 dígitos
                descricao="Produto Teste",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
            )

    def test_quantidade_negativa(self):
        """Deve rejeitar quantidade negativa"""
        with pytest.raises(ValueError):
            ProdutoNfce(
                ncm="84431000",
                cfop="5102",
                descricao="Produto Teste",
                quantidade=-1.0,
                valor_unitario=Decimal("100.00"),
            )

    def test_valor_total_produto(self):
        """Deve calcular valor total corretamente"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=2.0,
            valor_unitario=Decimal("50.00"),
        )
        assert produto.valor_total() == Decimal("100.00")

    def test_origem_invalida(self):
        """Deve rejeitar origem maior que 8"""
        with pytest.raises(ValueError, match="0 e 8"):
            ProdutoNfce(
                ncm="84431000",
                cfop="5102",
                descricao="Produto Teste",
                quantidade=1.0,
                valor_unitario=Decimal("100.00"),
                origem="9"  # Inválido, máximo é 8
            )


class TestConsumidorNfce:
    """Testes para modelo de Consumidor"""

    def test_consumidor_cpf_valido(self):
        """Deve aceitar CPF com 11 dígitos"""
        consumidor = ConsumidorNfce(cpf_cnpj="12345678901")
        assert consumidor.cpf_cnpj == "12345678901"

    def test_consumidor_cnpj_valido(self):
        """Deve aceitar CNPJ com 14 dígitos"""
        consumidor = ConsumidorNfce(cpf_cnpj="12345678901234")
        assert consumidor.cpf_cnpj == "12345678901234"

    def test_consumidor_cpf_invalido_10_digitos(self):
        """Deve rejeitar CPF com 10 dígitos"""
        with pytest.raises(ValueError, match="11 dígitos|14 dígitos"):
            ConsumidorNfce(cpf_cnpj="1234567890")

    def test_consumidor_nao_numerico(self):
        """Deve rejeitar CPF/CNPJ com caracteres"""
        with pytest.raises(ValueError, match="apenas dígitos"):
            ConsumidorNfce(cpf_cnpj="123.456.789-01")


class TestEmitenteNfce:
    """Testes para modelo de Emitente"""

    def test_emitente_valido(self):
        """Deve aceitar emitente com dados válidos"""
        emitente = EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja Teste",
            razao_social="Loja Teste LTDA",
            endereco="Rua das Flores",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="SP",
            cep="01234567",
        )
        assert emitente.cnpj == "06117114000172"
        assert emitente.uf == "SP"

    def test_cnpj_invalido_13_digitos(self):
        """Deve rejeitar CNPJ com 13 dígitos"""
        with pytest.raises(ValueError, match="14 dígitos"):
            EmitenteNfce(
                cnpj="0611711400017",  # Só 13
                ie="123456789012",
                nome_fantasia="Loja Teste",
                razao_social="Loja Teste LTDA",
                endereco="Rua das Flores",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="01234567",
            )

    def test_cep_invalido_7_digitos(self):
        """Deve rejeitar CEP com 7 dígitos"""
        with pytest.raises(ValueError, match="8 dígitos"):
            EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Loja Teste",
                razao_social="Loja Teste LTDA",
                endereco="Rua das Flores",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="SP",
                cep="0123456",  # Só 7
            )

    def test_uf_invalida(self):
        """Deve rejeitar UF inválida"""
        with pytest.raises(ValueError, match="UF inválida"):
            EmitenteNfce(
                cnpj="06117114000172",
                ie="123456789012",
                nome_fantasia="Loja Teste",
                razao_social="Loja Teste LTDA",
                endereco="Rua das Flores",
                numero="100",
                bairro="Centro",
                municipio="São Paulo",
                uf="XX",  # Inválida
                cep="01234567",
            )

    def test_uf_lowercase_convertida_uppercase(self):
        """Deve converter UF para maiúscula"""
        emitente = EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja Teste",
            razao_social="Loja Teste LTDA",
            endereco="Rua das Flores",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="sp",  # Minúscula
            cep="01234567",
        )
        assert emitente.uf == "SP"


class TestNfcePayload:
    """Testes para payload completo de NFC-e"""

    @pytest.fixture
    def emitente_padrao(self):
        """Emitente padrão para testes"""
        return EmitenteNfce(
            cnpj="06117114000172",
            ie="123456789012",
            nome_fantasia="Loja Teste",
            razao_social="Loja Teste LTDA",
            endereco="Rua das Flores",
            numero="100",
            bairro="Centro",
            municipio="São Paulo",
            uf="SP",
            cep="01234567",
        )

    @pytest.fixture
    def produto_padrao(self):
        """Produto padrão para testes"""
        return ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
        )

    def test_nfce_valida_completa(self, emitente_padrao, produto_padrao):
        """Deve aceitar NFC-e com dados válidos"""
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto_padrao],
        )
        assert len(payload.produtos) == 1
        assert payload.serie_nfce == 65

    def test_nfce_sem_produtos(self, emitente_padrao):
        """Deve rejeitar NFC-e sem produtos"""
        with pytest.raises(ValueError, match="at least 1 item"):
            NfcePayload(
                emitente=emitente_padrao,
                produtos=[],  # Vazio!
            )

    def test_nfce_serie_sempre_65(self, emitente_padrao, produto_padrao):
        """NFC-e deve sempre ter série 65"""
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto_padrao],
            serie_nfce=65,
        )
        assert payload.serie_nfce == 65

    def test_valor_total_produtos(self, emitente_padrao):
        """Deve calcular valor total de produtos corretamente"""
        produto1 = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto 1",
            quantidade=2.0,
            valor_unitario=Decimal("50.00"),
        )
        produto2 = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto 2",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
        )
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto1, produto2],
        )
        # (2 * 50) + (1 * 100) = 200
        assert payload.valor_total_produtos() == Decimal("200.00")

    def test_valor_total_icms(self, emitente_padrao):
        """Deve calcular ICMS total corretamente"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            aliquota_icms=18.0,
        )
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto],
        )
        # 100 * 18% = 18
        assert payload.valor_total_icms() == Decimal("18.00")

    def test_valor_total_pis(self, emitente_padrao):
        """Deve calcular PIS total corretamente"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            aliquota_pis=7.65,
        )
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto],
        )
        # 100 * 7.65% = 7.65
        assert payload.valor_total_pis() == Decimal("7.65")

    def test_valor_total_cofins(self, emitente_padrao):
        """Deve calcular COFINS total corretamente"""
        produto = ProdutoNfce(
            ncm="84431000",
            cfop="5102",
            descricao="Produto Teste",
            quantidade=1.0,
            valor_unitario=Decimal("100.00"),
            aliquota_cofins=7.65,
        )
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto],
        )
        # 100 * 7.65% = 7.65
        assert payload.valor_total_cofins() == Decimal("7.65")

    def test_nfce_com_consumidor(self, emitente_padrao, produto_padrao):
        """Deve aceitar NFC-e com consumidor"""
        consumidor = ConsumidorNfce(cpf_cnpj="12345678901234")
        payload = NfcePayload(
            emitente=emitente_padrao,
            produtos=[produto_padrao],
            consumidor=consumidor,
        )
        assert payload.consumidor is not None
        assert payload.consumidor.cpf_cnpj == "12345678901234"


class TestNfceIntegracao:
    """Testes de integração (dados realistas)"""

    def test_nfce_cenario_real_acougue(self):
        """Simular cenário real: venda em açougue"""
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
                email="contato@acougue.com.br",
            ),
            produtos=[
                ProdutoNfce(
                    ncm="02012100",  # Carne bovina
                    cfop="5102",
                    descricao="Carne Vermelha Premium",
                    quantidade=2.5,
                    valor_unitario=Decimal("45.90"),
                    aliquota_icms=18.0,
                ),
                ProdutoNfce(
                    ncm="02011000",  # Carne de porco
                    cfop="5102",
                    descricao="Carne de Porco",
                    quantidade=1.0,
                    valor_unitario=Decimal("25.50"),
                    aliquota_icms=18.0,
                ),
            ],
            consumidor=ConsumidorNfce(cpf_cnpj="12345678901"),
        )

        assert len(payload.produtos) == 2
        # (2.5 * 45.90) + (1.0 * 25.50) = 114.75 + 25.50 = 140.25
        assert payload.valor_total_produtos() == Decimal("140.25")
