# 📋 ERP Prado da Costa — Documentação de Contexto

## 1. VISÃO GERAL DO PROJETO

**Sistema:** ERPNext v17 (Frappe Framework) customizado para cenário fiscal brasileiro
**Repositório:** `erp_pradodacosta` (fork do ERPNext oficial)
**Objetivo:** PDV (Ponto de Venda) completo com emissão de NFC-e, integração com SEFAZ, e módulo fiscal brasileiro

### Stack Tecnológica

| Componente | Tecnologia | Versão |
|------------|-----------|--------|
| **Framework** | Frappe (Python) | v17 |
| **ERP** | ERPNext | latest (docker) |
| **Banco principal** | MariaDB | 10.11 |
| **Banco alternativo** | PostgreSQL | 15 (opcional) |
| **Cache/Queue** | Redis | 7 Alpine |
| **API Fiscal** | FastAPI (Python) | 2.0.0 |
| **Biblioteca fiscal** | erpbrasil.edoc | 3.1.1 |
| **Containerização** | Docker + Compose | v5 |
| **OS Produção** | Ubuntu 22.04 (VPS Hetzner) | — |

---

## 2. ESTRUTURA DE ARQUIVOS

```
📁 erp_pradodacosta/
├── docker-compose.yml           ← Orquestração principal (5 serviços)
├── .env.example                 ← Exemplo de configuração
│
├── acbr-container/              ← Container de serviços fiscais brasileiros
│   ├── Dockerfile               ← Python 3.11 + dependências
│   ├── requirements.txt         ← erpbrasil.edoc, reportlab, zeep, etc.
│   ├── api/
│   │   ├── main.py              ← API FastAPI (8 endpoints REST)
│   │   ├── validadores.py       ← Validação CPF/CNPJ (Python puro)
│   │   ├── formatadores.py      ← Formatação CPF/CNPJ/CEP
│   │   ├── nfe_controller.py    ← Controller NF-e (via erpbrasil.edoc)
│   │   └── nfce_controller.py   ← Controller NFC-e (via erpbrasil.edoc)
│   └── config/
│       ├── acbr_nfe.ini         ← Configuração NF-e
│       └── acbr_nfce.ini        ← Configuração NFC-e
│
├── erpnext/regional/brazil/     ← Módulo Brazil (customizado)
│   ├── __init__.py              ← v1.0.0
│   ├── setup.py                 ← Cria campos fiscais (NCM, CFOP, CST)
│   ├── acbr_bridge.py           ← Bridge Python → ACBr API HTTP
│   ├── validadores.py           ← Validação local (fallback offline)
│   ├── formatadores.py          ← Valor por extenso, formatação docs
│   └── nfce_controller.py       ← Controller que integra PDV → NFC-e
│
├── init-scripts/
│   └── init_frappe.sh           ← Script de boot do ERPNext
│
├── CONTEXTO.md                  ← Este arquivo
└── README-TESTE.md              ← Guia rápido de testes
```

---

## 3. ARQUITETURA DO SISTEMA

```
                   ┌─────────────────────────────────────┐
                   │          Navegador (Web)             │
                   │        http://localhost:8000         │
                   └──────────────┬──────────────────────┘
                                  │
┌─────────────────────────────────┼──────────────────────────┐
│                          DOCKER                           │
│                                                           │
│  ┌──────────────────┐    ┌──────────────────┐             │
│  │   erp-erpnext    │    │   erp-acbr       │             │
│  │                  │    │                  │             │
│  │  ERPNext/Frappe  │────▶   FastAPI        │             │
│  │  Porta 8000      │    │  Porta 8080      │             │
│  │                  │    │                  │             │
│  │  bench serve     │    │  erpbrasil.edoc  │             │
│  │  Gunicorn        │    │  NF-e / NFC-e    │             │
│  │  MariaDB         │    │  CPF/CNPJ        │             │
│  │  Redis           │    │  DANFE/PDF       │             │
│  └────────┬─────────┘    └────────┬─────────┘             │
│           │                       │                       │
│           ▼                       ▼                       │
│  ┌──────────────┐    ┌──────────────────────────┐         │
│  │  erp-mariadb │    │  erp-redis-cache          │         │
│  │  Porta 3307  │    │  Porta 6379               │         │
│  │  MariaDB 10  │    │  Redis 7                  │         │
│  └──────────────┘    └──────────────────────────┘         │
│                                                           │
│  ┌──────────────────┐                                     │
│  │  erp-postgres    │  (Opcional - não usado atualmente)  │
│  │  Porta 5433      │                                     │
│  └──────────────────┘                                     │
└───────────────────────────────────────────────────────────┘
```

---

## 4. DIÁRIO DE PROBLEMAS E SOLUÇÕES

### 🔴 Problema 1: PostgreSQL vs MariaDB

**Sintoma:**
A imagem oficial `frappe/erpnext:latest` usa MariaDB interno e não suporta PostgreSQL como banco primário.

**Tentativas frustradas:**
1. ❌ Configurar `frappe.Dockerfile` customizado com `psycopg2` — imagem base `frappe/frappe-worker:v16` não existia
2. ❌ Tentar `bench new-site --db-type postgres` dentro do container — o Frappe não conecta porque o MariaDB está em container separado

**Solução final:**
✅ Usar MariaDB como banco principal (padrão da imagem oficial)
✅ PostgreSQL mantido como container extra para uso futuro
✅ Removido `erpnext_data` volume e scripts de init customizados

**Arquivos alterados:** `docker-compose.yml`, removido `frappe.Dockerfile`

---

### 🔴 Problema 2: Container ERPNext reiniciando em loop

**Sintoma:**
O container `erp-erpnext` vivia em loop de restart. Logs mostravam:
```
"Worker failed to boot"
"Procfile does not exist or is not a file"
```

**Causa raiz:**
O `init-scripts/init_frappe.sh` usava `set -e` e `bench start` — quando qualquer comando falhava (ex: `bench drop-site`), o script inteiro encerrava, causando restart.

**Solução:**
1. ✅ Remover `set -e` do script (usar `|| true` para ignorar erros controlados)
2. ✅ Substituir `bench start` (que exige Procfile) por `bench serve --port 8000` (modo dev do Frappe)
3. ✅ Criar diretórios de log que estavam faltando (`/home/frappe/logs`)

**Arquivos alterados:** `init-scripts/init_frappe.sh`

---

### 🔴 Problema 3: Gunicorn ausente no container

**Sintoma:**
```
/bin/sh: 1: gunicorn: not found
```

**Causa:**
A imagem `frappe/erpnext:latest` é uma imagem de deploy que já tem gunicorn, mas quando usamos `bench start`, ele procura gunicorn no virtual env, não no sistema.

**Tentativas:**
1. ❌ `pip install gunicorn` dentro do script — instalava mas não achava
2. ❌ Criar Procfile manual — funcionava mas outros erros apareciam

**Solução final:**
✅ Usar `bench serve --port 8000` — servidor de desenvolvimento embutido do Frappe (Werkzeug)
✅ Aceitar o warning "This is a development server" (OK para ambiente local/de testes)

---

### 🔴 Problema 4: Assets não compilados (bundled_assets.json ausente)

**Sintoma:**
```
GET / → 500 Internal Server Error
bundled_assets.get(path) → AttributeError: 'NoneType' object has no attribute 'get'
```

**Causa:**
A imagem `frappe/erpnext:latest` não compila os assets CSS/JS automaticamente. O arquivo `bundled_assets.json` não é gerado.

**Solução:**
✅ Executar `bench build` manualmente dentro do container (compila ~35 assets, 33 segundos)
✅ O build gera todos os bundles: `website.bundle.css`, `login.bundle.css`, `desk.bundle.js`, etc.
✅ Também compila as traduções (32 idiomas, incluindo pt_BR)

**Comando usado:**
```bash
docker exec erp-erpnext bash -c \
  "cd /home/frappe/frappe-bench && source env/bin/activate && bench build"
```

---

### 🔴 Problema 5: ACBrLib não conseguia baixar do SourceForge

**Sintoma:**
```
>>> Aviso: Não foi possível baixar a ACBrLib automaticamente.
```

**Causa:**
SourceForge bloqueia downloads via script (HTTP 403 Forbidden)

**Solução:**
✅ Substituir ACBrLib (DLL C++) por `erpbrasil.edoc` (biblioteca Python pura)
✅ `erpbrasil.edoc` 3.1.1 + `cryptography` + `signxml` + `zeep` = stack completo para NF-e/NFC-e
✅ 100% Python, funciona em qualquer Linux, sem DLL

**Arquivos alterados:**
- `acbr-container/Dockerfile` — removeu dependência do ACBrLib
- `acbr-container/requirements.txt` — adicionou erpbrasil.edoc
- `acbr-container/api/main.py` — versão 2.0.0 com endpoints reais

---

### 🔴 Problema 6: Porta 5432 ocupada no Windows

**Sintoma:**
```
Error response from daemon: Bind for 0.0.0.0:5432 failed: port is already allocated
```

**Causa:**
O WSL/Docker do Windows já usa a porta 5432 internamente

**Solução:**
✅ Mapear PostgreSQL para porta externa 5433 (em vez de 5432)
```yaml
ports:
  - "5433:5432"
```

---

### 🔴 Problema 7: Site do ERPNext sendo recriado a cada restart

**Sintoma:**
O site `erp.pradodacosta.local` era recriado toda vez que o container reiniciava, causando retrabalho de instalação.

**Causa:**
O script `init_frappe.sh` verificava se o site existia mas o `set -e` matava o processo antes de chegar na verificação.

**Solução:**
✅ Adicionar verificação condicional robusta:
```bash
if [ ! -d "erp.pradodacosta.local" ]; then
    bench new-site ...
fi
```
✅ Verificar se o app ERPNext já está instalado antes de reinstalar:
```bash
APPS=$(python3 -c "import json; ...")
if echo "$APPS" | grep -q "erpnext"; then
    echo "✓ ERPNext já instalado!"
else
    bench --site ... install-app erpnext
fi
```

---

## 5. ENDPOINTS DISPONÍVEIS

### ERPNext (porta 8000)
| Rota | Método | Descrição |
|------|--------|-----------|
| `/api/method/frappe.ping` | GET | Health check → `{"message":"pong"}` |
| `/login` | GET | Página de login (200 ✅ após build) |
| `/app` | GET | Desk do Frappe (React SPA) |

### API ACBr (porta 8080)
| Rota | Método | Descrição | Status |
|------|--------|-----------|--------|
| `/health` | GET | Status da API e bibliotecas | ✅ |
| `/validar/documento` | POST | Valida CPF/CNPJ | ✅ |
| `/nfe/emitir` | POST | Emitir NF-e (precisa certificado) | 🟡 |
| `/nfce/emitir` | POST | Emitir NFC-e (precisa certificado) | 🟡 |
| `/nfe/consultar` | GET | Consultar NF-e na SEFAZ | 🟡 |
| `/nfe/cancelar` | POST | Cancelar NF-e | 🟡 |
| `/danfe/gerar` | POST | Gerar DANFE PDF | 🟡 |
| `/ncm/{ncm}` | GET | Consultar NCM | 🟡 |
| `/cfop/{cfop}` | GET | Consultar CFOP | 🟡 |

---

## 6. COMANDOS ÚTEIS

```bash
# Ver status dos containers
docker compose ps

# Ver logs do ERPNext
docker logs erp-erpnext --tail 50

# Ver logs da API ACBr
docker logs erp-acbr --tail 50

# Recompilar assets (se algo quebrar no CSS/JS)
docker exec erp-erpnext bash -c "cd /home/frappe/frappe-bench && source env/bin/activate && bench build"

# Acessar o container ERPNext
docker exec -it erp-erpnext bash

# Parar tudo
docker compose down

# Parar tudo e limpar volumes (cuidado: apaga dados)
docker compose down -v

# Subir apenas serviços específicos
docker compose up -d mariadb redis-cache acbr
```

---

## 7. PRODUÇÃO — PLANO DE DEPLOY

### Infraestrutura recomendada
```
VPS: Hetzner CX22 (€8/mês ≈ R$50)
  2 vCPU · 4GB RAM · 40GB SSD · Ubuntu 22.04
```

### Passos
1. Contratar VPS e instalar Docker
2. Clonar repositório
3. Ajustar variáveis de ambiente
4. Subir com `docker compose up -d`
5. Configurar SSL com Let's Encrypt (Nginx reverso)
6. Backup automático diário

### Custos estimados
| Item | Custo |
|------|-------|
| VPS Hetzner | ~R$50/mês |
| Domínio (.com.br) | ~R$3,50/mês |
| Certificado A1 | ~R$200/ano |
| **Total** | **~R$70/mês** |

---

## 8. LIÇÕES APRENDIDAS

1. **Sempre verificar se o site já existe** antes de criar — `if [ -d "site.local" ]` evita reinstalações infinitas
2. **Usar `|| true`** em scripts bash para evitar que erros controlados matem o processo
3. **Preferir `bench serve`** em vez de `bench start` / gunicorn para desenvolvimento local
4. **ACBrLib é problemática** em Linux/container — preferir `erpbrasil.edoc` que é 100% Python
5. **A imagem oficial `frappe/erpnext:latest`** não compila assets automaticamente — `bench build` é necessário
6. **MariaDB é o banco padrão** do ERPNext — PostgreSQL requer configuração adicional não trivial
7. **Sempre mapear portas conflitantes** do Windows (5432→5433)
8. **Logs salvam vidas** — `docker logs` é a primeira ferramenta de debug

---

## 9. STATUS ATUAL (18/06/2026)

| Requisito | Status | Observação |
|-----------|--------|------------|
| ERPNext rodando | ✅ | Porta 8000 |
| Página de login | ✅ | 200 OK (28KB) |
| API REST | ✅ | `frappe.ping` responde |
| API ACBr v2 | ✅ | Porta 8080, erpbrasil.edoc |
| Validação CPF/CNPJ | ✅ | Endpoint funcional |
| PostgreSQL | 🟢 | Porta 5433 (opcional) |
| MariaDB | ✅ | Porta 3307 |
| Redis | ✅ | Porta 6379 |
| NF-e real | 🟡 | Precisa certificado digital |
| NFC-e real | 🟡 | Precisa certificado digital |
| Impressão térmica | 🟡 | CUPS instalado, falta configurar |
| SSL/HTTPS | ❌ | Para produção |
| Backup automático | ❌ | Para produção |