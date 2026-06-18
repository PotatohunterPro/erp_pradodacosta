# 📝 CHANGELOG — ERP Prado da Costa

**Formato:** [UNRELEASED] | [X.Y.Z] — YYYY-MM-DD  
**Estilo:** [Conventional Commits](https://www.conventionalcommits.org/)

---

## [UNRELEASED]

### 🎯 Fase 1: Correções Críticas ✅ CONCLUÍDA

#### ✅ Corrigido
- **setup.py**: Tipos de campo incorretos (`Data` → `Char`)
  - NCM, CEST, CFOP_DEFAULT: agora aceitam apenas 4-8 dígitos
  - CPF_CNPJ, IE_RG, SUFRAMA: agora armazenam corretamente
  - Chaves de acesso e protocolos: agora usam `Char` para melhor validação
  - QR Code NFC-e: alterado para `Code` (armazena dados estruturados)

#### 📚 Documentação
- **docs/CERTIFICADO_A1.md**: Guia completo de provisioning
  - 12 seções: tipos, cartórios, custos, aquisição, Docker, SEFAZ
  - Troubleshooting com 5 cenários comuns
  - Referências de 4 autoridades certificadoras brasileiras
  - Instruções de volume mount e variáveis de ambiente

#### 🔧 Infraestrutura
- **docker-compose.yml**: Health checks adicionados
  - ERPNext: `/api/method/frappe.ping` (30s)
  - ACBr: `/health` (30s)
  - MariaDB: `mysqladmin ping` (10s)
  - PostgreSQL: `pg_isready` (10s)
  - Redis: `redis-cli ping` (10s)

#### ⚙️ Configuração
- **.env**: Template com variáveis sensíveis
  - Certificado digital (path, senha, datas de validade)
  - SEFAZ (ambiente, estado)
  - Banco de dados (MariaDB, PostgreSQL)
  - Redis, ACBr, logging
  - Adicionado ao `.gitignore`

- **.gitignore**: Arquivos sensíveis ignorados
  - `.env`, `.env.local`
  - `certs/`, `*.pfx`, `*.p12`
  - `logs/`, `*.log`
  - `backups/`, `*.bak`

#### 📋 Planejamento
- **TODO.md**: 60+ tarefas em 7 fases
  - Fase 1 (4/4): ✅ Concluída
  - Fase 2 (5 tasks): Implementação erpbrasil.edoc
  - Fase 3 (3 tasks): Tabelas fiscais (NCM, CFOP)
  - Fase 4 (3 tasks): Validações
  - Fase 5 (4 tasks): Testes automatizados
  - Fase 6 (4 tasks): Documentação
  - Fase 7 (3 tasks): Produção/CI-CD

### 🔄 Refatoração

Nenhuma refatoração significativa nesta versão.

### ⚠️ Problemas Conhecidos

1. **NFC-e/NF-e ainda são stubs**
   - Controllers retornam erro: "Not implemented"
   - Falta implementação com `erpbrasil.edoc`
   - Bloqueador para qualquer emissão real

2. **Certificado digital obrigatório**
   - Sem certificado A1, não é possível assinar documentos
   - Necessário adquirir em cartório (custo ~R$150-350/ano)

3. **SEFAZ em testes**
   - Ambiente padrão é homologação
   - Trocar para produção requer testes bem-sucedidos

### 🚀 Próximas Prioridades

1. **Fase 2**: Implementar geradores XML (erpbrasil.edoc)
2. **Fase 2**: Integrar assinatura digital (signxml)
3. **Fase 2**: Conectar com SEFAZ webservice
4. **Fase 5**: Criar testes automatizados (cobertura 80%+)

---

## [0.0.0] — 2024-01-01

### 🎯 Inicial
- Estrutura base do projeto (Docker + ERPNext + ACBr)
- Módulo Brasil com campos customizados
- API ACBr com endpoints stub
- Documentação inicial (CONTEXTO.md)

---

## 📊 Estatísticas

| Métrica | Valor |
|---------|-------|
| Commits da Fase 1 | 1 |
| Arquivos modificados | 5 |
| Arquivos criados | 2 |
| Linhas adicionadas | 789 |
| Linhas removidas | 13 |
| Documentação (linhas) | 480 (CERTIFICADO_A1.md) |

---

## 🔗 Referências

- **Branch**: `claude/laughing-archimedes-mcavq1`
- **Commit inicial**: `34b6a5c`
- **Data**: 18/06/2026
- **Status**: Em desenvolvimento

---

## 📌 Notas de Lançamento

### Para a próxima release:
- [ ] Implementar geradores XML
- [ ] Integrar SEFAZ webservice
- [ ] Criar testes automatizados
- [ ] Documentar deploy em produção
- [ ] Configurar CI/CD

### Requisitos para produção:
- [ ] Certificado digital A1 (adquirido e validado)
- [ ] Testes E2E em SEFAZ homologação
- [ ] Backup automático configurado
- [ ] SSL/HTTPS ativo
- [ ] Monitoramento em lugar
