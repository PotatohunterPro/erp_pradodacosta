# 🌐 AUDITORIA: TRADUÇÃO DO DOCTYPE CUSTOMER PARA PT-BR

## 📊 RESUMO
- **Total de campos**: 58
- **Todos em inglês**: ✓ 100%
- **Severidade**: 🔴 CRÍTICA (usuário vê tudo em EN)

---

## 📋 MAPEAMENTO COMPLETO DE TRADUÇÕES

| # | Label Atual (EN) | Tradução Sugerida (PT-BR) | Campo | Tipo |
|----|-----------------|------------------------|-------|------|
| 1 | Series | Série | naming_series | Select |
| 2 | Customer Name | Nome do Cliente | customer_name | Data |
| 3 | Gender | Sexo | gender | Link |
| 4 | Customer Type | Tipo de Cliente | customer_type | Select |
| 5 | Default Company Bank Account | Conta Bancária Padrão da Empresa | default_bank_account | Link |
| 6 | Lead | Oportunidade | lead_name | Link |
| 7 | Image | Imagem | image | Attach Image |
| 8 | Account Manager | Gerente da Conta | account_manager | Link |
| 9 | Customer Group | Grupo de Clientes | customer_group | Link |
| 10 | Territory | Território | territory | Link |
| 11 | Tax ID | ID Fiscal / CPF/CNPJ | tax_id | Data |
| 12 | Tax Category | Categoria Fiscal | tax_category | Link |
| 13 | Disabled | Desativado | disabled | Check |
| 14 | Is Internal Customer | É Cliente Interno | is_internal_customer | Check |
| 15 | Represents Company | Representa Empresa | represents_company | Link |
| 16 | Allowed To Transact With | Permitido Transacionar Com | companies | Table |
| 17 | Billing Currency | Moeda de Faturamento | default_currency | Link |
| 18 | Default Price List | Lista de Preços Padrão | default_price_list | Link |
| 19 | Print Language | Idioma de Impressão | language | Link |
| 20 | Address HTML | Endereço HTML | address_html | HTML |
| 21 | Website | Site | website | Data |
| 22 | Contact HTML | Contato HTML | contact_html | HTML |
| 23 | Customer Primary Contact | Contato Principal do Cliente | customer_primary_contact | Link |
| 24 | Mobile No | Telefone Celular | mobile_no | Read Only |
| 25 | Email Id | E-mail | email_id | Read Only |
| 26 | Customer Primary Address | Endereço Principal do Cliente | customer_primary_address | Link |
| 27 | Primary Address | Endereço Principal | primary_address | Text Editor |
| 28 | Accounts | Contas | accounts | Table |
| 29 | Default Payment Terms Template | Modelo de Termos de Pagamento Padrão | payment_terms | Link |
| 30 | Customer Details | Detalhes do Cliente | customer_details | Text |
| 31 | Market Segment | Segmento de Mercado | market_segment | Link |
| 32 | Industry | Indústria | industry | Link |
| 33 | Is Frozen | Bloqueado | is_frozen | Check |
| 34 | Loyalty Program | Programa de Fidelidade | loyalty_program | Link |
| 35 | Loyalty Program Tier | Nível do Programa de Fidelidade | loyalty_program_tier | Data |
| 36 | Sales Partner | Parceiro de Vendas | default_sales_partner | Link |
| 37 | Commission Rate | Taxa de Comissão | default_commission_rate | Float |
| 38 | Sales Team | Equipe de Vendas | sales_team | Table |
| 39 | Customer POS ID | ID do PDV do Cliente | customer_pos_id | Data |
| 40 | Credit Limit | Limite de Crédito | credit_limits | Table |
| 41 | Allow Sales Invoice Creation Without Sales Order | Permitir Criar Fatura Sem Pedido de Venda | so_required | Check |
| 42 | Allow Sales Invoice Creation Without Delivery Note | Permitir Criar Fatura Sem Nota de Entrega | dn_required | Check |
| 43 | Tax Withholding Category | Categoria de Retenção Fiscal | tax_withholding_category | Link |
| 44 | Opportunity | Oportunidade | opportunity_name | Link |
| 45 | Address & Contact | Endereço & Contato | contact_and_address_tab | Tab |
| 46 | Settings | Configurações | settings_tab | Tab |
| 47 | Sales Team | Equipe de Vendas | sales_team_tab | Tab |
| 48 | Accounting | Contabilidade | accounting_tab | Tab |
| 49 | Tax | Impostos | tax_tab | Tab |
| 50 | Portal Users | Usuários do Portal | portal_users_tab | Tab |
| 51 | Customer Portal Users | Usuários do Portal do Cliente | portal_users | Table |
| 52 | Prospect | Prospecto | prospect_name | Link |
| 53 | First Name | Primeiro Nome | first_name | Data |
| 54 | Last Name | Sobrenome | last_name | Data |
| 55 | Supplier Numbers | Números do Fornecedor | supplier_numbers | Table |
| 56 | Tax Withholding Group | Grupo de Retenção Fiscal | tax_withholding_group | Link |
| 57 | More Info | Mais Informações | more_info_tab | Tab |
| 58 | Connections | Conexões | connections_tab | Tab |

---

## 🚨 CAMPOS CRÍTICOS (Para usuário final)

Esses campos aparecem **no formulário visível ao usuário**:

### Aba Básica
- ✗ Customer Name → **Nome do Cliente**
- ✗ Customer Type → **Tipo de Cliente**
- ✗ Gender → **Sexo**
- ✗ Customer Group → **Grupo de Clientes**
- ✗ Territory → **Território**

### Aba Endereço & Contato
- ✗ Mobile No → **Telefone Celular**
- ✗ Email Id → **E-mail**
- ✗ Website → **Site**
- ✗ Primary Address → **Endereço Principal**

### Aba Impostos
- ✗ Tax ID → **CPF/CNPJ**
- ✗ Tax Category → **Categoria Fiscal**
- ✗ Tax Withholding Category → **Categoria de Retenção**

### Aba Contabilidade
- ✗ Billing Currency → **Moeda de Faturamento**
- ✗ Default Payment Terms Template → **Termos de Pagamento Padrão**
- ✗ Credit Limit → **Limite de Crédito**

### Aba Configurações
- ✗ Disabled → **Desativado**
- ✗ Is Frozen → **Bloqueado**

---

## ✅ PRÓXIMOS PASSOS

Você quer que eu:

**Opção A:** Traduza APENAS o **customer.json** agora
- Tempo: ~30 minutos
- Resultado: Customer totalmente em PT-BR

**Opção B:** Procure e traduza TODOS os DocTypes brasileiros
- Procurar por: `brazil`, `fiscal`, `nfe`, `nfce`, `icms`, `pis`, `cofins`
- Tempo: ~3-4 horas
- Resultado: Sistema inteiro em PT-BR

**Opção C:** Traduza toda a interface ERPNext (todas as abas, campos, botões)
- Tempo: ~1 semana
- Resultado: Sistema 100% PT-BR

---

Qual opção prefere? Recomendo **Opção B** para focar nos pontos fiscais. 🎯
