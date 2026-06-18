# 🤖 AGENTS.md — Contexto, Regras e Método de Trabalho

**Este documento é a referência principal para qualquer agente de IA operando neste repositório.**  
**Deve ser lido integralmente antes de qualquer tarefa.**

---

## 1. Objetivo do Projeto

O projeto é um **Sistema ERP customizado** baseado em ERPNext v17 (Frappe Framework) com foco em emissão de documentos fiscais brasileiros (NF-e/NFC-e) e gestão de PDV (Ponto de Venda).

### Visão
Fornecer um ERP acessível, containerizado e pronto para produção que integra:
- Frappe/ERPNext como core
- Serviços fiscais brasileiros (SEFAZ)
- PDV com emissão de NFC-e
- Validações e formatações brasileiras

### Prioridade Atual
1. **Implementação completa de NFC-e/NF-e** (bloqueador crítico)
2. Integração SEFAZ com certificado digital A1
3. Testes automatizados (cobertura mínima 80%)
4. Deploy em produção (VPS + SSL)

### NÃO é prioridade atual
- Multi-tenancy sofisticado
- Editor avançado de templates
- Integração com múltiplas transportadoras
- Features que não estejam no MVP

---

## 2. Papéis Esperados do Agente

Ao atuar neste projeto, a IA deve se comportar simultaneamente como:

### 2.1 Full Stack Engineer
Responsável por implementar, refatorar e manter código Python (Frappe), FastAPI (ACBr) e infraestrutura Docker.

**Expectativas:**
- Código legível, modular e bem estruturado
- Seguir padrões Frappe e FastAPI
- Documentação inline onde necessário
- Evitar duplicação de código

### 2.2 Fiscal/Compliance Engineer
Responsável por entender regras fiscais brasileiras (SEFAZ, NF-e, NFC-e, impostos).

**Expectativas:**
- Validar campos fiscais conforme tabelas SEFAZ
- Entender fluxo NFC-e (layout 4.0)
- Conhecer requisistos de certificado digital A1
- Documentar decisões de design fiscal

### 2.3 Security & Compliance Reviewer
Responsável por revisar segurança de certificados, assinatura digital, acesso a dados e logs.

**Expectativas:**
- Validar manejo de certificados (nunca logar ou expor)
- Revisar permissões de arquivo/container
- Auditar fluxo de dados sensíveis
- Testar com dados de teste (nunca dados reais)

### 2.4 DevOps & Infrastructure
Responsável por manter Docker, CI/CD, backup, monitoramento e deploy.

**Expectativas:**
- Health checks funcionando
- Volumes persistidos corretamente
- Logs acessíveis e não expondo secrets
- Rollback possível em qualquer versão

### 2.5 QA Lead
Responsável por testes, validação de fluxos e redução de bugs em produção.

**Expectativas:**
- TDD first: testes antes da implementação
- Cobertura mínima 80%
- Cenários: happy path, error, empty, loading
- Validação manual antes de concluir task

---

## 3. Regras de Ouro

### 3.1 Proibido "Vibe Coding"
Toda alteração deve ser:
- **Contextual**: justificada pela análise do problema
- **Rastreável**: visível em commit message e PR
- **Coerente**: alinhada com arquitetura existente

### 3.2 TDD First é Obrigatório
Fluxo obrigatório para implementação:
1. Entender o problema (ler CONTEXTO.md, TODO.md)
2. Resumir regras aplicáveis (fiscal, segurança, arquitetura)
3. Propor plano de testes (o que vai testar?)
4. Criar testes que FALHAM (red)
5. Implementar o mínimo necessário (green)
6. Refatorar sem excesso (refactor)

### 3.3 Proibido Feature Creep
- Não criar feature grande fora do escopo da tarefa
- Não adicionar dependências sem justificativa forte
- Não alterar schema/certificado/segurança sem explicação clara

### 3.4 Dívida Técnica
- Toda dívida identificada deve ser registrada em TODO.md
- Comentários com `TODO:` devem indicar linha e contexto
- Não deixar código quebrado ou "quase funciona"

### 3.5 Certificado Digital é Crítico
- **Nunca logar** certificado ou senha em nenhuma circunstância
- **Nunca testar** com dados reais (só com SEFAZ de testes)
- **Sempre validar** se certificado é válido antes de usar
- **Sempre usar** volume mount (não COPY no Dockerfile)

---

## 4. Stack e Convenções Técnicas

### 4.1 Stack Principal

| Componente | Tecnologia | Versão |
|-----------|-----------|--------|
| **Framework Web** | Frappe (Python) | v17 |
| **ERP** | ERPNext | latest (docker) |
| **API Fiscal** | FastAPI | 2.0.0 |
| **Biblioteca Fiscal** | erpbrasil.edoc | 3.1.1+ |
| **Banco Principal** | MariaDB | 10.11 |
| **Cache/Queue** | Redis | 7 Alpine |
| **Containerização** | Docker + Compose | v5+ |
| **Assinatura Digital** | signxml + cryptography | 41.0.0+ |

### 4.2 Estrutura de Módulos

```
erpnext/regional/brazil/     ← Customizações Frappe (886 linhas)
├── __init__.py              ← Setup e hooks
├── setup.py                 ← Criação de campos customizados
├── nfce_controller.py       ← Controller POS → NFC-e
├── acbr_bridge.py           ← Cliente HTTP para ACBr
├── validadores.py           ← Validações locais (fallback)
└── formatadores.py          ← Formatações brasileiras

acbr-container/             ← Serviços Fiscais (624 linhas)
├── api/main.py              ← Endpoints FastAPI (8 rotas)
├── api/nfce_controller.py   ← Lógica NFC-e (a implementar)
├── api/nfe_controller.py    ← Lógica NF-e (a implementar)
├── api/validadores.py       ← Validação CPF/CNPJ puro
├── api/formatadores.py      ← Formatadores
└── Dockerfile               ← Python 3.11 slim
```

### 4.3 Convenções Python

**Frappe/ERPNext:**
```python
# Sempre usar frappe.* para acesso ao framework
frappe.get_doc('POS Invoice', name)
frappe.db.get_value('Item', {'ncm': ncm})
frappe.throw(msg, exc=frappe.ValidationError)
frappe.log_error(msg, title)
```

**FastAPI/ACBr:**
```python
# Usar Pydantic para validação
from pydantic import BaseModel, Field

class NfcePayload(BaseModel):
    cnpj: str = Field(..., regex=r'^\d{14}$')
    produtos: list[ProdutoPayload]
    
# Sempre usar try/except com tipos específicos
try:
    resultado = processar()
except erpbrasil.edoc.exceptions.AssinaturaError as e:
    raise HTTPException(status_code=400, detail=str(e))
```

### 4.4 Convenções de Arquivo

**Certificados e Segurança:**
```bash
certs/                      ← Never commit, add to .gitignore
  certificado.pfx          ← Volume mount em docker-compose.yml
  
.env                        ← Never commit, use .env.example como template
CERT_PASSWORD=...          ← Usar environment variables, nunca hardcode
```

**Logs:**
```bash
logs/                       ← Diretório de logs (não commitar)
  acbr.log                 ← Log do container ACBr
  nfce_emissoes.log        ← Log de emissões (sem dados sensíveis)
```

---

## 5. Segurança Digital

### 5.1 Checklist de Segurança para Toda Tarefa

Antes de qualquer implementação, validar:

- [ ] **Certificado Digital**
  - Nunca logar certificado ou senha
  - Sempre usar volume mount
  - Validar expiração antes de usar
  - Testar com SEFAZ homologação antes de produção

- [ ] **Autenticação Frappe**
  - Validar que user está logado antes de operações
  - Checar permissões (is_manager, custom roles)
  - Auditar quem emitiu qual NFC-e

- [ ] **Autorização**
  - Apenas proprietário da empresa pode emitir NFC-e
  - Apenas admin pode acessar configurações fiscais
  - Logs de quem cancelou ou alterou documento

- [ ] **Exposição de Erro**
  - Nunca expor stack trace ao usuário final
  - Erros técnicos → logs apenas
  - Mensagem amigável ao usuário final
  - SEFAZ errors → logar raw, mostrar code amigável

- [ ] **Redirecionamentos**
  - Validar que URL é interna (não abrir qualquer URL)
  - Checar se documento existe antes de redirecionar
  - Fallback seguro se documento não encontrado

- [ ] **Dados Sensíveis**
  - CPF/CNPJ: nunca logar completo (mascarar: `***.***.***-**`)
  - IE: nunca logar
  - Certificado: nunca logar (somente status: "válido até X")
  - API keys: usar secrets manager, nunca em .env commitado

- [ ] **Testes**
  - Usar SEFAZ ambiente de testes (não produção)
  - Usar CNPJ/CPF fictícios (não reais)
  - Usar certificado de testes (não A1 real)

---

## 6. Fluxo de Desenvolvimento

### 6.1 Antes de Começar Qualquer Task

1. **Ler CONTEXTO.md** — entender arquitetura e histórico
2. **Ler TODO.md** — ver status do projeto
3. **Ler AGENTS.md** — este arquivo
4. **Ler commit message** — entender último estado

### 6.2 Ao Iniciar Task

```markdown
## Análise Inicial

### Resumo da tarefa
[1-2 sentences do que precisa fazer]

### Regras aplicáveis
- Regra fiscal 1
- Regra de segurança 1
- Padrão de código 1

### Plano de testes
1. Teste unitário: [o que vai testar?]
2. Teste integração: [cenário de sucesso?]
3. Teste erro: [o que espera se falhar?]

### Riscos percebidos
- Risco 1: [impacto] (probabilidade)
- Risco 2: [impacto] (probabilidade)
```

### 6.3 Durante Implementação

- Criar testes que FALHAM primeiro
- Implementar mínimo necessário
- Refatorar se necessário
- Executar `pytest` ou `npm test` continuamente
- Não fazer commit até tudo verde

### 6.4 Antes de Fazer Commit

```bash
# 1. Testes devem passar
pytest tests/

# 2. Linting deve passar
pylint erpnext/regional/brazil/ acbr-container/api/

# 3. Type checking (se usando TypeScript ou mypy)
mypy .

# 4. Build Docker (se alterou Dockerfile)
docker build acbr-container/

# 5. Validar que não logou secrets
grep -r "CERT_PASSWORD\|senha\|secret" . --include="*.py"
```

### 6.5 Commit Message

```
feat(nfce): implementar geração XML com erpbrasil.edoc

- Criar classe NfceGenerator com validações
- Integrar signxml para assinatura
- Testar com SEFAZ homologação
- Adicionar logging (sem expor certificado)

Closes #123
Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>
```

---

## 7. Fases de Desenvolvimento

### Fase 1: ✅ Correções Críticas (CONCLUÍDA)
- [x] Tipos de campo
- [x] Documentação certificado
- [x] .env e health checks

### Fase 2: 🔄 Implementação erpbrasil.edoc (EM PROGRESSO)
- [ ] Geração XML NFC-e
- [ ] Geração XML NF-e
- [ ] Assinatura digital
- [ ] Integração SEFAZ

### Fase 3: 📋 Tabelas Fiscais
- [ ] Popular NCM
- [ ] Popular CFOP
- [ ] Integrar IBPT

### Fase 4: ✔️ Validações
- [ ] IE por UF
- [ ] Valor por extenso
- [ ] Plano de contas

### Fase 5: 🧪 Testes
- [ ] Testes unitários (80%+)
- [ ] Testes integração
- [ ] Testes E2E
- [ ] Testes carga

### Fase 6: 📚 Documentação
- [ ] Deploy produção
- [ ] Guia desenvolvimento
- [ ] Atualizar CONTEXTO.md

### Fase 7: 🚀 Produção
- [ ] CI/CD (GitHub Actions)
- [ ] Monitoramento
- [ ] Backup automático

---

## 8. O que Fazer vs O que NÃO Fazer

### ✅ FAÇA

- Ler TODO.md antes de cada tarefa
- Documentar decisões de design fiscal
- Testar com dados fictícios (nunca reais)
- Logar erros sem expor secrets
- Usar volume mount para certificados
- Validar inputs com Pydantic/Frappe
- Commitar frequentemente com mensagens claras
- Pedir ajuda se não souber (não quebrar produção)

### ❌ NÃO FAÇA

- "Vibe coding" sem análise
- Adicionar feature fora do escopo
- Testar com dados reais de clientes
- Logar certificado, senha ou PIX-key
- Hardcode passwords em código
- Usar `pickle` para dados sensíveis
- Fazer refatoração gigante sem necessidade
- Commitar sem passar em testes
- Ignorar warnings de segurança
- Deixar TODOs sem registrar em TODO.md

---

## 9. Padrões de Resposta do Agente

### Antes de Implementar

```markdown
## 📋 Análise da Tarefa

### Resumo
[1-2 sentences]

### Regras Aplicáveis
- [Lista de regras de AGENTS.md, CONTEXTO.md ou TODO.md]

### Plano TDD
1. **Teste Unitário**: [o que?]
2. **Teste Integração**: [o que?]
3. **Teste de Erro**: [o que?]

### Riscos Percebidos
- [Risco]: [impacto] ([probabilidade])

### Implementação Proposta
- [Passo 1]
- [Passo 2]
```

### Depois de Implementar

```markdown
## ✅ Tarefa Concluída

### O que foi alterado
- [Arquivo 1]: [o quê?]
- [Arquivo 2]: [o quê?]

### Testes criados/ajustados
- [Test 1]: [o quê testa?]
- [Test 2]: [o quê testa?]

### Validações
- ✅ Testes passando
- ✅ Lint ok
- ✅ Build ok
- ✅ Sem secrets expostos

### Limitações/Riscos Restantes
- [Limitação 1]: [por quê?]
- [Risco residual 1]: [por quê?]

### Próximo Passo
[Qual task de TODO.md vem depois?]
```

---

## 10. Definição de "Pronto"

Uma tarefa só é considerada **PRONTA** quando:

- [ ] Resolve o problema descrito na tarefa
- [ ] Não cria regressão óbvia em features existentes
- [ ] Segue TDD first (testes antes/durante implementação)
- [ ] Respeita segurança prática (sem exposição de secrets)
- [ ] Mantém coerência com arquitetura existente
- [ ] Passa em testes (unit/integration/lint/build)
- [ ] Commit message é clara e rastreável
- [ ] Documentação foi atualizada (se necessário)
- [ ] Validação manual foi feita (se possível)

---

## 11. Referências Rápidas

### Estrutura de Pastas
```
erp_pradodacosta/
├── CONTEXTO.md                    # Histórico e arquitetura
├── AGENTS.md                      # Este arquivo
├── TODO.md                        # Roadmap de tarefas
├── CHANGELOG.md                   # Histórico de mudanças
├── docker-compose.yml             # Orquestração (5 serviços)
├── .env                          # Variáveis sensíveis (não commitar)
├── .env.example                  # Template público
├── erpnext/regional/brazil/      # Módulo Frappe
└── acbr-container/               # Container ACBr (FastAPI)
    ├── api/main.py               # 8 endpoints REST
    └── Dockerfile                # Python 3.11 slim
```

### Links Importantes
- **ERPNext Docs**: https://docs.erpnext.com/
- **Frappe Framework**: https://frappe.io/
- **erpbrasil.edoc**: https://github.com/harenson/erpbrasil.edoc
- **SEFAZ**: https://www.sefaz.fazenda.gov.br/
- **Manual NF-e**: http://www.nfe.fazenda.gov.br/

### Comandos Úteis
```bash
# Ler contexto do projeto
cat CONTEXTO.md
cat TODO.md
cat AGENTS.md

# Docker
docker-compose up -d           # Subir tudo
docker-compose down            # Parar tudo
docker logs erp-acbr --tail 50 # Logs

# Teste
pytest tests/ -v               # Rodar testes
pytest --cov                   # Cobertura

# Lint
pylint erpnext/regional/brazil/
flake8 acbr-container/api/
```

---

## 12. Contato e Escalação

Se não souber ou encontrar bloqueador:
1. Documentar o problema em TODO.md
2. Criar issue/task descritiva
3. Solicitar revisão antes de continuar
4. **NÃO quebrar produção para "aprender"**

---

**Última atualização:** 18/06/2026  
**Responsável:** Claude Code  
**Status:** ✅ Em vigor para Fase 2
