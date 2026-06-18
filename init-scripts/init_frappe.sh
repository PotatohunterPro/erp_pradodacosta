#!/bin/bash
# Sem set -e para evitar reinícios desnecessários

echo "══════════════════════════════════════════════════"
echo "  ERP Prado da Costa - Inicialização do Frappe"
echo "══════════════════════════════════════════════════"

# Aguardar MariaDB
echo ">>> Aguardando MariaDB..."
until mysqladmin ping -h mariadb -u root -padmin123 --silent 2>/dev/null; do
    sleep 2
done
echo "✓ MariaDB pronto!"

# Configurações via common_site_config.json (nunca falha)
echo ">>> Configurando ambiente..."
cd /home/frappe/frappe-bench/sites

# Ler configuração atual ou criar
if [ ! -f "common_site_config.json" ]; then
    echo '{}' > common_site_config.json
fi

# Usar python para configurar (evita erros do bench)
python3 -c "
import json
with open('common_site_config.json', 'r+') as f:
    cfg = json.load(f)
    cfg['db_host'] = 'mariadb'
    cfg['db_port'] = 3306
    cfg['db_type'] = 'mariadb'
    cfg['redis_cache'] = 'redis://redis-cache:6379'
    cfg['redis_queue'] = 'redis://redis-cache:6379'
    cfg['redis_socketio'] = 'redis://redis-cache:6379'
    cfg['developer_mode'] = 1
    f.seek(0)
    json.dump(cfg, f, indent=4)
    f.truncate()
"
echo "✓ Configuração OK!"

# Criar site se não existe
if [ ! -d "erp.pradodacosta.local" ]; then
    echo ">>> Criando site: erp.pradodacosta.local"
    bench new-site erp.pradodacosta.local \
        --mariadb-root-password admin123 \
        --admin-password admin123 || {
        echo "⚠️ Erro ao criar site. Tentando novamente..."
        sleep 3
        bench new-site erp.pradodacosta.local \
            --mariadb-root-password admin123 \
            --admin-password admin123
    }
    echo "✓ Site criado!"
fi

# Configurar Redis no site (se falhar, ignora)
if [ -f "erp.pradodacosta.local/site_config.json" ]; then
    python3 -c "
import json
with open('erp.pradodacosta.local/site_config.json', 'r+') as f:
    cfg = json.load(f)
    cfg['redis_cache'] = 'redis://redis-cache:6379'
    cfg['redis_queue'] = 'redis://redis-cache:6379'
    cfg['redis_socketio'] = 'redis://redis-cache:6379'
    cfg['developer_mode'] = 1
    f.seek(0)
    json.dump(cfg, f, indent=4)
    f.truncate()
"
fi

# Verificar se ERPNext está instalado
if [ -f "erp.pradodacosta.local/site_config.json" ]; then
    APPS=$(python3 -c "import json; cfg=json.load(open('erp.pradodacosta.local/site_config.json')); print(','.join(cfg.get('installed_apps',[])))" 2>/dev/null)
    if echo "$APPS" | grep -q "erpnext"; then
        echo "✓ ERPNext já instalado!"
    else
        echo ">>> Instalando ERPNext (leva ~5 min)..."
        bench --site erp.pradodacosta.local install-app erpnext || {
            echo "⚠️ Falha na instalação, tentando novamente..."
            bench --site erp.pradodacosta.local install-app erpnext
        }
        echo "✓ ERPNext instalado!"
    fi
fi

cd /home/frappe/frappe-bench
bench use erp.pradodacosta.local 2>/dev/null || true

echo ""
echo "══════════════════════════════════════════════════"
echo "  ✅ Servidor iniciando!"
echo "  🌐 http://localhost:8000"
echo "  👤 Administrator / admin123"
echo "══════════════════════════════════════════════════"
echo ""

# Ativar ambiente virtual e iniciar servidor
source env/bin/activate 2>/dev/null || true
cd /home/frappe/frappe-bench

echo ">>> Iniciando Frappe na porta 8000..."
exec bench serve --port 8000