"""
Testes para Tabelas de Conformidade Fiscal Brasileira

Valida:
- Tabelas de ICMS por NCM e UF
- Validação de CST ICMS, PIS, COFINS
- Validação de Regime Tributário
- Alíquotas conforme legislação
"""

import pytest
from decimal import Decimal
from api.icms_tabelas import (
    obter_aliquota_icms,
    validar_cst_icms,
    validar_cst_pis,
    validar_cst_cofins,
    validar_regime_tributario,
    obter_descricao_cst_icms,
    obter_descricao_cst_pis,
    obter_descricao_cst_cofins,
    obter_descricao_regime,
    RegimeTributario,
)


class TestIcmsAliquotas:
    """Testes para alíquotas dinâmicas de ICMS"""

    def test_icms_carne_bovina_sp(self):
        """Carne bovina em SP deve ter 12% ICMS"""
        aliquota = obter_aliquota_icms("02012100", "SP")
        assert aliquota == Decimal("12.00")

    def test_icms_carne_bovina_rj(self):
        """Carne bovina no RJ deve ter 20% ICMS"""
        aliquota = obter_aliquota_icms("02012100", "RJ")
        assert aliquota == Decimal("20.00")

    def test_icms_equipamentos_sp(self):
        """Equipamentos em SP devem ter 18% ICMS"""
        aliquota = obter_aliquota_icms("84431000", "SP")
        assert aliquota == Decimal("18.00")

    def test_icms_ncm_nao_encontrado(self):
        """NCM não cadastrado deve retornar 18% (padrão)"""
        aliquota = obter_aliquota_icms("99999999", "SP")
        assert aliquota == Decimal("18.00")

    def test_icms_diferentes_estados(self):
        """Mesmo NCM pode ter alíquotas diferentes em diferentes estados"""
        icms_sp = obter_aliquota_icms("02012100", "SP")
        icms_rj = obter_aliquota_icms("02012100", "RJ")
        assert icms_sp != icms_rj
        assert icms_sp == Decimal("12.00")
        assert icms_rj == Decimal("20.00")


class TestCstIcms:
    """Testes para validação de CST ICMS"""

    def test_cst_00_valido(self):
        """CST 00 (Tributada integralmente) deve ser válido"""
        assert validar_cst_icms("00") is True

    def test_cst_30_valido(self):
        """CST 30 (Isenta) deve ser válido"""
        assert validar_cst_icms("30") is True

    def test_cst_40_valido(self):
        """CST 40 (Não tributada) deve ser válido"""
        assert validar_cst_icms("40") is True

    def test_cst_icms_invalido(self):
        """CST ICMS inválido deve retornar False"""
        assert validar_cst_icms("99") is False

    def test_cst_icms_all_valid(self):
        """Todos os CST ICMS válidos devem passar"""
        valid_csts = ["00", "10", "20", "30", "40", "41", "50", "51", "60", "70", "90"]
        for cst in valid_csts:
            assert validar_cst_icms(cst) is True

    def test_obter_descricao_cst_icms(self):
        """Deve retornar descrição legível de CST ICMS"""
        desc = obter_descricao_cst_icms("00")
        assert desc == "Tributada integralmente"

    def test_obter_descricao_cst_icms_invalido(self):
        """Descrição de CST inválido deve ser None"""
        desc = obter_descricao_cst_icms("99")
        assert desc is None


class TestCstPis:
    """Testes para validação de CST PIS"""

    def test_cst_pis_01_valido(self):
        """CST PIS 01 deve ser válido"""
        assert validar_cst_pis("01") is True

    def test_cst_pis_07_valido(self):
        """CST PIS 07 (Isenta) deve ser válido"""
        assert validar_cst_pis("07") is True

    def test_cst_pis_invalido(self):
        """CST PIS inválido deve retornar False"""
        assert validar_cst_pis("11") is False

    def test_obter_descricao_cst_pis(self):
        """Deve retornar descrição legível de CST PIS"""
        desc = obter_descricao_cst_pis("01")
        assert desc is not None
        assert "operação tributável" in desc.lower()


class TestCstCofins:
    """Testes para validação de CST COFINS"""

    def test_cst_cofins_01_valido(self):
        """CST COFINS 01 deve ser válido"""
        assert validar_cst_cofins("01") is True

    def test_cst_cofins_07_valido(self):
        """CST COFINS 07 (Isenta) deve ser válido"""
        assert validar_cst_cofins("07") is True

    def test_cst_cofins_invalido(self):
        """CST COFINS inválido deve retornar False"""
        assert validar_cst_cofins("11") is False

    def test_obter_descricao_cst_cofins(self):
        """Deve retornar descrição legível de CST COFINS"""
        desc = obter_descricao_cst_cofins("01")
        assert desc is not None
        assert "operação tributável" in desc.lower()


class TestRegimeTributario:
    """Testes para validação de Regime Tributário"""

    def test_regime_simples_nacional(self):
        """Regime SN (Simples Nacional) deve ser válido"""
        assert validar_regime_tributario("SN") is True

    def test_regime_lucro_real(self):
        """Regime LR (Lucro Real) deve ser válido"""
        assert validar_regime_tributario("LR") is True

    def test_regime_lucro_presumido(self):
        """Regime LP (Lucro Presumido) deve ser válido"""
        assert validar_regime_tributario("LP") is True

    def test_regime_invalido(self):
        """Regime inválido deve retornar False"""
        assert validar_regime_tributario("XX") is False

    def test_obter_descricao_regime(self):
        """Deve retornar descrição legível de regime"""
        desc = obter_descricao_regime("SN")
        assert desc == "Simples Nacional"

    def test_obter_descricao_regime_invalido(self):
        """Descrição de regime inválido deve ser None"""
        desc = obter_descricao_regime("XX")
        assert desc is None

    def test_regime_enum(self):
        """RegimeTributario enum deve ter valores corretos"""
        assert RegimeTributario.SIMPLES_NACIONAL.value == "SN"
        assert RegimeTributario.LUCRO_REAL.value == "LR"
        assert RegimeTributario.LUCRO_PRESUMIDO.value == "LP"
