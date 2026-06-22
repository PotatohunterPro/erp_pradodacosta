"""
Controller NFC-e usando erpbrasil.edoc

Responsável por:
- Gerar XML conforme layout 4.0 SEFAZ
- Validar dados fiscais
- Retornar XML para assinatura
"""

import logging
from decimal import Decimal
from typing import Optional

from nfce_models import (
    ProdutoNfce,
    ConsumidorNfce,
    EmitenteNfce,
    NfcePayload
)
from nfce_generator import NfceGenerator

logger = logging.getLogger(__name__)


def emitir_nfce_via_edoc(request) -> dict:
    """
    Gera XML para NFC-e (cupom fiscal eletrônico)

    Fluxo:
    1. Converter dados de request para modelos validados
    2. Gerar XML conforme SEFAZ layout 4.0
    3. Calcular chave de acesso
    4. Retornar XML (assinatura feita em módulo separado)

    Args:
        request: EmitirNFeRequest com dados da venda

    Returns:
        dict com status, XML gerado e erros (se houver)
    """
    try:
        logger.info("Iniciando geração de XML NFC-e")

        # 1. Validar e converter request em modelos Pydantic
        payload = _converter_request_para_nfce_payload(request)
        logger.info(f"Payload validado: {len(payload.produtos)} produtos")

        # 2. Gerar XML
        generator = NfceGenerator()
        xml_nfce = generator.gerar_xml(payload)
        logger.info("XML NFC-e gerado com sucesso")

        # 3. Gerar chave de acesso
        chave_acesso = generator.gerar_chave_nfce(payload)
        logger.info(f"Chave NFC-e gerada: {chave_acesso}")

        # 4. Validar XML
        if not generator.validar_xml(xml_nfce):
            logger.warning("XML gerado não passou em validação")
            return {
                "sucesso": False,
                "erros": ["XML gerado não é bem-formado"]
            }

        return {
            "sucesso": True,
            "chave_acesso": chave_acesso,
            "xml_assinado": xml_nfce,
            "numero": payload.numero_nfce,
            "erros": []
        }

    except ValueError as e:
        logger.error(f"Validação falhou: {str(e)}")
        return {
            "sucesso": False,
            "erros": [f"Erro de validação: {str(e)}"]
        }
    except Exception as e:
        logger.error(f"Erro ao gerar NFC-e: {str(e)}", exc_info=True)
        return {
            "sucesso": False,
            "erros": [f"Erro interno: {str(e)}"]
        }


def _converter_request_para_nfce_payload(request) -> NfcePayload:
    """
    Converte EmitirNFeRequest para NfcePayload validado

    TODO: Integrar com Frappe para buscar dados automáticos
    """

    # Dados do emitente (TODO: obter de configuração)
    emitente = EmitenteNfce(
        cnpj=request.config.cnpj_emitente or "06117114000172",
        ie=request.config.ie_emitente or "123456789012",
        nome_fantasia="Loja PDV",
        razao_social="Loja PDV LTDA",
        endereco="Rua Exemplo",
        numero="100",
        bairro="Centro",
        municipio="São Paulo",
        uf="SP",
        cep="01234567",
    )

    # Converter produtos
    produtos = []
    for prod in request.produtos:
        produtos.append(ProdutoNfce(
            ncm=prod.ncm or "00000000",
            cfop=prod.cfop or "5102",
            descricao=prod.descricao,
            quantidade=prod.quantidade,
            valor_unitario=Decimal(str(prod.valor_unitario)),
            aliquota_icms=18.0,  # TODO: obter de NCM ou configuração
        ))

    # Consumidor (opcional)
    consumidor = None
    if request.destinatario_cpf_cnpj and request.destinatario_cpf_cnpj != "00000000000":
        consumidor = ConsumidorNfce(
            cpf_cnpj=request.destinatario_cpf_cnpj,
            nome=request.destinatario_nome,
        )

    # Montar payload
    payload = NfcePayload(
        emitente=emitente,
        produtos=produtos,
        consumidor=consumidor,
        observacao=request.informacoes_complementares or None,
    )

    return payload