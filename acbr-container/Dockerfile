# ============================================================
# Container ACBr - Serviços Fiscais Brasileiros (Python puro)
# ============================================================
FROM python:3.11-slim

LABEL org.opencontainers.image.title="ACBr Fiscal Services - ERP Prado da Costa"
LABEL org.opencontainers.image.description="Serviços fiscais brasileiros usando erpbrasil.edoc (100% Python)"
LABEL org.opencontainers.image.source="https://github.com/PotatohunterPro/erp_pradodacosta"

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    libssl-dev \
    libxml2-dev \
    libxslt1-dev \
    wget \
    curl \
    ca-certificates \
    cups \
    cups-client \
    && rm -rf /var/lib/apt/lists/*

# Criar diretórios
RUN mkdir -p /opt/acbr/{certificados,config,logs,xmls,darfes}

# Copiar dependências Python
COPY requirements.txt /opt/acbr/requirements.txt
RUN pip install --no-cache-dir -r /opt/acbr/requirements.txt

# Copiar API
COPY api/ /opt/acbr/api/
COPY config/ /opt/acbr/config/

WORKDIR /opt/acbr

EXPOSE 8080

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8080", "--log-level", "info"]