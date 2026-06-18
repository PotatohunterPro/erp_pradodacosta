# ============================================================
# Dockerfile customizado para ERPNext com PostgreSQL
# Baseado na imagem oficial frappe/bench
# ============================================================
FROM frappe/frappe-worker:v16

LABEL org.opencontainers.image.title="ERP Prado da Costa - Frappe + PostgreSQL"
LABEL org.opencontainers.image.description="ERPNext customizado com PostgreSQL, módulo Brazil e ACBr"

USER root

# Instalar dependências do PostgreSQL
RUN apt-get update && apt-get install -y \
    postgresql-client \
    libpq-dev \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Instalar psycopg2 (driver PostgreSQL para Python)
RUN pip install psycopg2-binary && \
    pip install requests

# Criar diretórios
RUN mkdir -p /home/frappe/frappe-bench/apps/erpnext/erpnext/regional/brazil

# Copiar módulo Brazil (será montado como volume, mas ter uma cópia base)
COPY erpnext/regional/brazil/ /home/frappe/frappe-bench/apps/erpnext/erpnext/regional/brazil/

# Script de entrada
COPY init-scripts/init_frappe.sh /init_frappe.sh
RUN chmod +x /init_frappe.sh

USER frappe

WORKDIR /home/frappe/frappe-bench

EXPOSE 8000 9000

ENTRYPOINT ["/init_frappe.sh"]