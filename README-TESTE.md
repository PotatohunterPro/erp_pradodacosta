# 🧪 Como testar o sistema ERP Prado da Costa

## Pré-requisitos
- Docker Desktop instalado e rodando
- Git

## Passo a passo

### 1. Containers já rodando (ACBr + PostgreSQL + Redis)
```bash
docker compose ps

# Você verá:
# erp-acbr        -> API ACBr (NF-e, NFC-e, CPF/CNPJ)
# erp-postgres    -> PostgreSQL 15
# erp-redis-cache -> Redis 7
```

### 2. Testar API ACBr (já funcional)
```bash
# Health Check
curl http://localhost:8080/health
# Resposta: {"status":"ok","versao_acbr":"1.0.0","versao_api":"1.0.0"}

# Validar CPF
curl -X POST http://localhost:8080/validar/documento \
  -H "Content-Type: application/json" \
  -d '{"documento":"529.982.247-25"}'
# Resposta: {"valido":true,"tipo":"CPF","formatado":"529.982.247-25",...}

# Acessar documentação Swagger
# Abra no navegador: http://localhost:8080/docs
```

### 3. Conectar ao PostgreSQL
```bash
# Conectar via psql (se instalado localmente):
psql -h localhost -p 5433 -U frappe_user -d erp_pradodacosta
# Senha: frappe_pass_123
```

### 4. Ambiente visual da estrutura
![Estrutura do Projeto](docs/estrutura.png)

## Arquivos criados

| Arquivo | Descrição |
|---------|-----------|
| `docker-compose.yml` | Orquestração completa: Postgres + Redis + Frappe + ACBr |
| `acbr-container/Dockerfile` | Container ACBr (validação fiscal, NF-e, NFC-e) |
| `acbr-container/api/main.py` | API REST com FastAPI (8 endpoints fiscais) |
| `erpnext/regional/brazil/` | Módulo Brazil (setup, bridge ACBr, validadores) |
| `.env.example` | Configuração de ambiente |

## Para subir o ERPNext completo

O ERPNext é um sistema grande (~2GB de imagem). Temos duas formas:

### A) Via Docker (recomendado para teste final)
```bash
docker compose up -d frappe
```
Isso baixará a imagem oficial do ERPNext (~2GB) e configurará o site.
Acesse: http://localhost:8000
Login: Administrator / admin123

### B) Via Frappe Bench (recomendado para desenvolvimento)
```bash
# Instalar Frappe Bench (dentro de um container Linux)
docker run -it --rm -v .:/workspace frappe/bench bash
# Dentro do container:
bench init frappe-bench
cd frappe-bench
bench new-site site1.local --db-type postgres --db-host host.docker.internal:5433
bench get-app erpnext
bench --site site1.local install-app erpnext
bench start
```

## Testes rápidos da API

```powershell
# Validar CPF (Windows PowerShell)
$body = @{documento='529.982.247-25'} | ConvertTo-Json
Invoke-WebRequest -Uri 'http://localhost:8080/validar/documento' `
  -Method Post -Body $body -ContentType 'application/json' | Select-Object -ExpandProperty Content

# Health Check
Invoke-WebRequest 'http://localhost:8080/health' | Select-Object -ExpandProperty Content