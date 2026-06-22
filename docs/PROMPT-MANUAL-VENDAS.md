# 📋 PROMPT — Manual de Configuração do ERP Prado da Costa para Vendas Simples

**Use este prompt para solicitar o manual de configuração no chat Claude**

---

## 🎯 PROMPT PARA COPIAR E COLAR

```markdown
# Manual de Configuração — ERP Prado da Costa para Vendas Simples

## 🏪 Nosso Cenário

Somos uma pequena loja de varejo (açougue/mercearia/comércio) e queremos começar a:
- ✅ Vender produtos no PDV (Ponto de Venda)
- ✅ Emitir NFC-e (Nota Fiscal de Consumidor Eletrônica)
- ✅ Controlar estoque básico
- ✅ Receber pagamentos em dinheiro/cartão
- ❌ Não precisa de: multi-loja, multi-empresa, relatórios complexos, contabilidade avançada

## 📝 O que queremos saber

1. **Checklist de Pré-requisitos**
   - Quais dados/documentos precisamos ter antes de começar?
   - Onde obter/cadastrar certificado digital A1?
   - Qual é o custo inicial (licenses, certificado, etc)?
   - Quanto tempo leva para preparar tudo?

2. **Guia Passo a Passo de Configuração Inicial**
   - Como instalar/subir o sistema (Docker)?
   - Como configurar a empresa principal?
   - Como cadastrar usuários vendedores?
   - Como cadastrar categoria de produtos?
   - Como cadastrar produtos com NCM/CFOP corretos?
   - Como configurar formas de pagamento?
   - Como testar emissão de NFC-e (sem certificado real)?

3. **Configuração Mínima para Primeira Venda**
   - Qual é o fluxo de uma venda simples (do início ao fim)?
   - Como abrir um PDV (Ponto de Venda)?
   - Como adicionar produtos ao carrinho?
   - Como finalizar uma venda?
   - Como imprimir cupom/NFC-e?
   - Onde fica o comprovante fiscal?

4. **Validações Fiscais Básicas**
   - O sistema valida dados automaticamente?
   - Quais campos são obrigatórios para emitir NFC-e?
   - Qual é a diferença entre NFC-e e NF-e para nosso caso?
   - Precisamos de certificado digital para começar a vender em testes?

5. **Integração com SEFAZ — Roadmap**
   - Por enquanto, podemos vender sem SEFAZ real (apenas PDV local)?
   - Quando precisamos do certificado A1 para começar?
   - Qual é o ambiente de testes SEFAZ (homologação)?
   - Quanto tempo leva para migrar de testes para produção?

6. **Suporte e Troubleshooting**
   - Se algo quebrar, como debugar?
   - Onde ficam os logs de vendas/erros?
   - Como fazer backup dos dados de vendas?
   - Como recuperar uma venda se o sistema cair?

## 📌 Contexto Adicional

- **Sistema:** ERPNext v17 + Container ACBr (NFC-e)
- **Infraestrutura:** Docker (5 containers: ERPNext, ACBr, MariaDB, Redis, PostgreSQL)
- **Status atual:** Fase 1 ✅ 100% | Fase 2 🔄 (em desenvolvimento)
- **Documentação disponível:**
  - CONTEXTO.md (arquitetura)
  - AGENTS.md (guia para agentes de IA)
  - docs/CERTIFICADO_A1.md (certificado digital)
  - TODO.md (roadmap completo)

## 🎯 Entrega Esperada

Por favor, crie um **manual em PT-BR com:**
- [ ] Checklist de pré-requisitos (formato tabela)
- [ ] Guia passo-a-passo com screenshots/exemplos
- [ ] Fluxo de primeira venda (diagrama ou lista)
- [ ] Seção FAQ com dúvidas comuns
- [ ] Links para recursos externos (SEFAZ, cartórios, etc)
- [ ] Arquivo MD pronto para documentação do projeto

## 📊 Formato Preferido

```
Manual-Configuracao-ERP-PradoCosta-v1.0.md

Sumário:
1. Pré-requisitos
2. Configuração Inicial
3. Primeira Venda
4. Validações Fiscais
5. Certificado Digital A1
6. Troubleshooting
7. FAQ
8. Próximos Passos
```

Obrigado! 🙏
```

---

## 💡 Dicas de Uso

**Opção 1: Use o prompt exato acima**
- Copie e cole no chat Claude
- Funciona como está!

**Opção 2: Customize conforme sua necessidade**
- Ajuste o cenário se for diferente (restaurante, farmácia, etc)
- Adicione perguntas específicas do seu negócio
- Mude formatos ou entrega esperada

**Opção 3: Envie por partes**
- Primeira mensagem: contexto + pré-requisitos
- Segunda: configuração inicial
- Terceira: primeira venda
- Assim o Claude entende melhor seu caso

---

## 📌 O que o Prompt Cobre

```
✅ Cenário do negócio (pequeno varejo)
✅ Objetivos claros (vender com NFC-e)
✅ Escopo limitado (não overengineering)
✅ Pré-requisitos (certificado, dados, custos)
✅ Passo-a-passo (instalação até primeira venda)
✅ Validações fiscais (NCM, CFOP, impostos)
✅ SEFAZ integration (testes + produção)
✅ Troubleshooting (quando algo quebrar)
✅ Contexto do projeto (stack, status, docs)
✅ Formato esperado (MD bem estruturado)
```

---

## 🎯 Resultado Esperado

O Claude vai criar para você:

📄 **Manual-Configuracao-ERP-PradoCosta-v1.0.md** com:

1. **Checklist Pré-requisitos**
   - [ ] Certificado A1
   - [ ] CNPJ/CPF da empresa
   - [ ] Produtos cadastrados com NCM
   - [ ] Etc.

2. **Guia Passo-a-Passo**
   - Como instalar (docker-compose up)
   - Como logar (admin / senha)
   - Como cadastrar primeiro produto
   - Como fazer primeira venda
   - Como emitir NFC-e

3. **Fluxo Visual**
   ```
   Abrir PDV → Selecionar produtos → Calcular impostos 
   → Finalizar venda → Gerar NFC-e → Imprimir cupom
   ```

4. **FAQ**
   - "Posso vender sem certificado?"
   - "Quanto custa tudo isso?"
   - "Quanto tempo leva?"
   - "E se a SEFAZ cair?"

5. **Próximos Passos**
   - Fase 2 (implementação real NFC-e)
   - Migração para produção
   - Treinamento da equipe

---

## ✨ Vantagem de Usar Este Prompt

✅ **Específico:** Não é genérico, é baseado no NOSSO sistema  
✅ **Estruturado:** Seções claras, fácil de acompanhar  
✅ **Prático:** Passo-a-passo, não teoria  
✅ **Documentado:** Referencia nosso projeto real  
✅ **Reutilizável:** Pode ser usado para treinar equipe  
✅ **PT-BR:** Em português, entendível para todos  

---

**Está pronto para usar! Copie, Cole e Peça! 🚀**
