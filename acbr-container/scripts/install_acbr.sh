#!/bin/bash
# ============================================================
# Script de instalação da ACBrLib no Linux
# ============================================================
set -e

ACBR_VERSION="1.0.0"
ACBR_URL="https://sourceforge.net/projects/acbr/files/ACBrLib/1.0.0/ACBrLib-${ACBR_VERSION}-linux-x64.tar.gz"
ACBR_LIB_DIR="/opt/acbr/lib"
TEMP_DIR="/tmp/acbr-install"

echo ">>> Baixando ACBrLib ${ACBR_VERSION}..."
mkdir -p ${TEMP_DIR}
cd ${TEMP_DIR}

# Tentar download do SourceForge
if wget -q --timeout=30 -O acbr.tar.gz "${ACBR_URL}"; then
    echo ">>> Extraindo ACBrLib..."
    tar -xzf acbr.tar.gz -C ${ACBR_LIB_DIR}
    echo ">>> ACBrLib extraída em ${ACBR_LIB_DIR}"
else
    echo ">>> Aviso: Não foi possível baixar a ACBrLib automaticamente."
    echo ">>> Crie manualmente a estrutura em ${ACBR_LIB_DIR}"
    echo ">>> Ou configure usando o script 'download_acbr.sh' manualmente"
    echo ""
    echo ">>> Criando estrutura de diretórios placeholder..."
    mkdir -p ${ACBR_LIB_DIR}
fi

# Verificar bibliotecas instaladas
echo ">>> Bibliotecas ACBr disponiveis:"
ls -la ${ACBR_LIB_DIR}/ || echo "(vazio - instalação manual necessaria)"

# Limpar
rm -rf ${TEMP_DIR}

echo ">>> Instalação ACBr concluída!"