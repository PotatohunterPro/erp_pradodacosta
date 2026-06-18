# 📋 TODO — Correções do Projeto ERP Prado da Costa

**Última atualização:** 18/06/2026  
**Status geral:** 9/60 tarefas concluídas (15%)

---

## 🔴 FASE 1: CORREÇÕES CRÍTICAS (Bloqueadores)

- [x] **1.1** Corrigir tipos de campo em `setup.py`
  - [x] Linhas 39-40: NCM e CEST de `Data` → `Char` com validação
  - [x] Linha 41: CFOP de `Data` → `Char`
  - [x] Arquivo: `erpnext/regional/brazil/setup.py`
  - [x] Prioridade: 🔴 ALTA
  - ✅ **CONCLUÍDO**

- [x] **1.2** Documentar provisioning de certificado digital A1
  - [x] Criar `docs/CERTIFICADO_A1.md` com passo a passo
  - [x] Incluir como carregar PFX em container Docker
  - [x] Incluir referências de cartórios recomendados
  - [x] Prioridade: 🔴 ALTA
  - ✅ **CONCLUÍDO** (guia completo com 12 seções)

- [x] **1.3** Criar template `.env` com valores reais
  - [x] Remover senhas hardcoded do `docker-compose.yml`
  - [x] Arquivo: `.env` (baseado em `.env.example`)
  - [x] Incluir paths para certificado PFX
  - [x] Prioridade: 🔴 ALTA
  - ✅ **CONCLUÍDO** (.env completo com variáveis de certificado)

- [x] **1.4** Adicionar health checks ao Docker Compose
  - [x] ERPNext: health check `/api/method/frappe.ping`
  - [x] ACBr: health check `/health`
  - [x] MariaDB: health check com `mysqladmin ping`
  - [x] PostgreSQL: health check com `pg_isready`
  - [x] Arquivo: `docker-compose.yml`
  - [x] Prioridade: 🟡 MÉDIA
  - ✅ **CONCLUÍDO**

---

## 🟡 FASE 2: IMPLEMENTAÇÃO erpbrasil.edoc

- [ ] **2.1** Implementar geração XML NFC-e
  - [ ] Arquivo: `acbr-container/api/nfce_controller.py`
  - [ ] Usar biblioteca `erpbrasil.edoc` (v3.1.1)
  - [ ] Gerar layout 4.0 válido
  - [ ] Testes com dados mock
  - [ ] Prioridade: 🔴 CRÍTICA

- [ ] **2.2** Implementar geração XML NF-e
  - [ ] Arquivo: `acbr-container/api/nfe_controller.py`
  - [ ] Usar biblioteca `erpbrasil.edoc` (v3.1.1)
  - [ ] Suportar NF-e com múltiplos produtos
  - [ ] Testes com dados mock
  - [ ] Prioridade: 🔴 CRÍTICA

- [ ] **2.3** Implementar assinatura digital XML
  - [ ] Arquivo: `acbr-container/api/assinador.py` (novo)
  - [ ] Carregar certificado PFX com senha
  - [ ] Assinar XML com `signxml`
  - [ ] Validar assinatura
  - [ ] Prioridade: 🔴 CRÍTICA

- [ ] **2.4** Implementar geração de QR Code NFC-e
  - [ ] Arquivo: `acbr-container/api/nfce_controller.py`
  - [ ] Gerar QR Code conforme SEFAZ
  - [ ] Retornar como base64 ou PNG
  - [ ] Prioridade: 🔴 CRÍTICA

- [ ] **2.5** Integrar com webservice SEFAZ (testes)
  - [ ] Arquivo: `acbr-container/api/sefaz_client.py` (novo)
  - [ ] Endpoint de transmissão de NFC-e
  - [ ] Endpoint de consulta de protocolo
  - [ ] Endpoint de cancelamento
  - [ ] Usar webservice de testes primeiro
  - [ ] Prioridade: 🔴 CRÍTICA

---

## 🟠 FASE 3: TABELAS FISCAIS

- [ ] **3.1** Popular tabela NCM
  - [ ] Arquivo: `acbr-container/api/tabelas_ncm.py` (novo)
  - [ ] Carregar dados de NCM (mínimo 100 itens)
  - [ ] Endpoint GET `/ncm/{codigo}` funcional
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **3.2** Popular tabela CFOP
  - [ ] Arquivo: `acbr-container/api/tabelas_cfop.py` (novo)
  - [ ] Carregar dados de CFOP (5000, 5100, 6000, 6100, etc)
  - [ ] Endpoint GET `/cfop/{codigo}` funcional
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **3.3** Integrar com IBPT (tabela federal de impostos)
  - [ ] Arquivo: `acbr-container/api/ibpt_client.py` (novo)
  - [ ] Consultar alíquotas por NCM
  - [ ] Cache de resultados (Redis)
  - [ ] Prioridade: 🟢 BAIXA (futuro)

---

## 🔵 FASE 4: VALIDAÇÕES

- [ ] **4.1** Implementar validação de IE por UF
  - [ ] Arquivo: `erpnext/regional/brazil/validadores.py`
  - [ ] Linha 66: Remover TODO e implementar
  - [ ] Criar arquivo `ie_validators_by_uf.py` (novo)
  - [ ] Validar IE/RG para cada estado
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **4.2** Expandir valor_por_extenso para valores maiores
  - [ ] Arquivo: `erpnext/regional/brazil/formatadores.py`
  - [ ] Linha 44: Remover TODO e expandir
  - [ ] Suportar até trilhões
  - [ ] Adicionar testes unitários
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **4.3** Implementar setup de plano de contas brasileiro
  - [ ] Arquivo: `erpnext/regional/brazil/setup.py`
  - [ ] Linhas 261-264: Remover `pass` e implementar
  - [ ] Criar contas contábeis padrão (SPED)
  - [ ] Prioridade: 🟡 MÉDIA

---

## 🟢 FASE 5: TESTES

- [ ] **5.1** Criar testes unitários do módulo Brazil
  - [ ] Arquivo: `erpnext/regional/brazil/tests/test_validadores.py` (novo)
  - [ ] Testar CPF/CNPJ válidos e inválidos
  - [ ] Testar IE por UF
  - [ ] Coverage mínimo 80%
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **5.2** Criar testes unitários ACBr API
  - [ ] Arquivo: `acbr-container/tests/test_main.py` (novo)
  - [ ] Testar endpoints com dados mock
  - [ ] Testar validação de entrada (Pydantic)
  - [ ] Coverage mínimo 80%
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **5.3** Testes de integração E2E
  - [ ] Arquivo: `tests/test_integration.py` (novo)
  - [ ] Teste NFC-e completo (geração → assinatura → resposta)
  - [ ] Teste com certificado de testes SEFAZ
  - [ ] Prioridade: 🟠 ALTA (após impl. SEFAZ)

- [ ] **5.4** Testes de carga
  - [ ] Ferramenta: `locust` ou `k6`
  - [ ] Simular 100 NFC-e simultâneas
  - [ ] Verificar limites de Redis/MariaDB
  - [ ] Prioridade: 🟢 BAIXA (produção)

---

## 🟣 FASE 6: DOCUMENTAÇÃO

- [ ] **6.1** Guia de Deploy em Produção
  - [ ] Arquivo: `docs/DEPLOY_PRODUCAO.md` (novo)
  - [ ] VPS Hetzner setup
  - [ ] SSL/HTTPS com Let's Encrypt
  - [ ] Backup automático
  - [ ] Monitoramento
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **6.2** Guia de Desenvolvimento
  - [ ] Arquivo: `docs/DESENVOLVIMENTO.md` (novo)
  - [ ] Como rodar localmente
  - [ ] Como adicionar novo endpoint
  - [ ] Como debugar NFC-e
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **6.3** Atualizar CONTEXTO.md
  - [ ] Adicionar seção de certificado digital
  - [ ] Atualizar status de implementação
  - [ ] Adicionar comandos úteis para certificado
  - [ ] Prioridade: 🟢 BAIXA

- [ ] **6.4** Atualizar README-TESTE.md
  - [ ] Remover seções obsoletas
  - [ ] Adicionar testes com certificado
  - [ ] Adicionar exemplos de payloads
  - [ ] Prioridade: 🟢 BAIXA

---

## 🚀 FASE 7: PRODUÇÃO

- [ ] **7.1** Configurar CI/CD (GitHub Actions)
  - [ ] Arquivo: `.github/workflows/test.yml` (novo)
  - [ ] Executar testes em cada push
  - [ ] Build e push para Docker Hub
  - [ ] Prioridade: 🟡 MÉDIA

- [ ] **7.2** Configurar monitoring
  - [ ] Datadog ou New Relic
  - [ ] Alertas para downtime
  - [ ] Logs centralizados
  - [ ] Prioridade: 🟢 BAIXA (futuro)

- [ ] **7.3** Configurar backup automático
  - [ ] Script: `scripts/backup.sh` (novo)
  - [ ] Backup diário de MariaDB
  - [ ] Armazenar em S3 ou similar
  - [ ] Prioridade: 🟡 MÉDIA

---

## 📊 RESUMO POR PRIORIDADE

### 🔴 CRÍTICA (Bloqueadores)
1. **1.1** - Corrigir tipos de campo
2. **1.2** - Documentar certificado
3. **1.3** - Criar .env
4. **2.1** - NFC-e XML
5. **2.2** - NF-e XML
6. **2.3** - Assinadura digital
7. **2.4** - QR Code
8. **2.5** - SEFAZ webservice

### 🟡 MÉDIA (Importante)
- 1.4, 3.1, 3.2, 4.1, 4.2, 4.3, 5.1, 5.2, 6.1, 6.2, 7.1, 7.3

### 🟢 BAIXA (Futuro)
- 3.3, 5.4, 6.3, 6.4, 7.2

---

## 🎯 MÉTRICAS

| Métrica | Alvo | Atual |
|---------|------|-------|
| Funcionalidades | 100% | 40% |
| Testes | 80% coverage | 0% |
| Documentação | Completa | 50% |
| Tempo estimado | — | 15 dias |

---

## 📝 NOTAS

- Começar pela **FASE 1** (correções críticas)
- Depois **FASE 2** (implementação real com erpbrasil.edoc)
- Certificado digital é **bloqueador** — solicitar com antecedência
- Usar ambiente de testes SEFAZ antes de produção
- Cada commit deve ter testes passando

---

**Status:** Em Progresso  
**Responsável:** Claude Code  
**Próxima revisão:** Após FASE 1
