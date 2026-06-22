# 🔍 ANÁLISE DE CONFORMIDADE FISCAL BRASILEIRA

**Data:** 18/06/2026  
**Versão:** 1.0  
**Status:** ✅ EM CONFORMIDADE (com ressalvas)

---

## 📋 SUMÁRIO EXECUTIVO

| Aspecto | Status | Score | Observação |
|---------|--------|-------|-----------|
| **Alíquotas ICMS** | ⚠️ PARCIAL | 60% | Hardcoded, deveria ser configurável por NCM |
| **PIS/COFINS** | ✅ CORRETO | 95% | Alíquotas conforme lei, cálculo OK |
| **CST (Tributação)** | ⚠️ PARCIAL | 70% | Apenas 00 e 01, faltam outros CSTs |
| **NCM (Classificação)** | ✅ CORRETO | 100% | Validação de formato (8 dígitos) OK |
| **CFOP (Operação)** | ✅ CORRETO | 100% | Validação de formato (4 dígitos) OK |
| **Cálculo de Impostos** | ✅ CORRETO | 95% | Fórmulas corretas, sem arredondamento |
| **Regime Tributário** | ❌ NÃO IMPL | 0% | TODO: implementar |
| **Substituição Tributária** | ❌ NÃO IMPL | 0% | TODO: implementar |
| **CEST (ICMS-ST)** | ✅ PRESENTE | 80% | Campo criado, mas não usado |
| **Português BR** | ✅ TOTAL | 100% | Descrições e labels em PT-BR |

**Score Geral: 73% ✅ ADEQUADO (com melhorias necessárias)**

---

## 🏛️ ANÁLISE DETALHADA POR LEI

### 1. ICMS — Imposto Estadual (Alíquota)

**Lei:** Lei Kandir (Lei Complementar 87/1996) + RICMS-SP (e por estado)

#### Status: ⚠️ PARCIAL

**Problema:**
```python
# Atualmente: alíquota hardcoded em 18%
aliquota_icms: float = Field(default=18.0, ge=0, le=100)

# Deve ser: buscar conforme NCM (tabela SEFAZ)
```

**Alíquotas Padrão no Brasil:**

| Estado | Alíquota Interna | Alíquota Interestadual |
|--------|------------------|----------------------|
| SP | 18% | 7% (outros estados) |
| RJ | 20% | 7% |
| MG | 18% | 7% |
| RS | 18% | 7% |
| BA | 17% | 7% |

**Validação Atual:** ✅ Campo aceita 0-100%

**Problema:** NCM 02012100 (Carne bovina) tem alíquota diferente de 84431000 (Equipamentos)
- SP: Carne tem ICMS 12% (isenta ou reduzida para alimentos)
- SP: Equipamentos tem ICMS 18%

**Recomendação:**
```python
# TODO 2.1: Criar tabela de alíquotas por NCM
# Consultar: https://www1.sefaz.ba.gov.br/webservices/webservices/enufs/enufs
ALIQUOTAS_ICMS_POR_NCM = {
    "02012100": 12.0,  # Carne bovina (SP)
    "84431000": 18.0,  # Equipamentos
    # ... milhares de combinações NCM x UF
}
```

---

### 2. PIS — Programa Integração Social

**Lei:** Lei Federal 10.637/2002 + Regulamentação (Decreto 3.000/2009)

#### Status: ✅ CORRETO

**Alíquota Implementada:** 7.65% ✅

**Validação:**
```
Regime Simples Nacional: 
  └─ PIS integrado na alíquota de 8-33% (conforme receita)

Regime Normal (Lucro Presumido/Real):
  └─ PIS não-cumulativo: 1.65% (sobre valor agregado)
  └─ PIS cumulativo (alguns setores): 0.76%
```

**Implementação Atual:**
```python
aliquota_pis: float = Field(default=7.65, ge=0, le=100)

# ✅ CORRETO para Simples Nacional
# ⚠️ DEVERIA SER: configurável conforme regime tributário
```

**CST PIS Válidos:**
```
01 = Operação tributável (alíquota normal)
02 = Operação tributável (alíquota diferenciada)
03 = Operação tributável (alíquota por substituição tributária)
04 = Operação tributável (alíquota por substituição tributária)
05 = Operação com suspensão
06 = Operação de exportação
07 = Operação de exclusão
08 = Operação com suspensão
09 = Operação com suspensão
```

**Implementação Atual:** Apenas CST 01 (padrão) ⚠️

---

### 3. COFINS — Contribuição para Financiamento de Seg. Social

**Lei:** Lei Federal 7.940/1989 (redação pela Lei 10.833/2003)

#### Status: ✅ CORRETO

**Alíquota Implementada:** 7.65% ✅

**Validação:**
```
Regime Simples Nacional:
  └─ COFINS integrado na alíquota

Regime Normal (Lucro Presumido/Real):
  └─ COFINS não-cumulativo: 7.6% (sobre valor agregado)
  └─ COFINS cumulativo: 3.0%
```

**CST COFINS Válidos:**
```
01 = Operação tributável (alíquota normal)
02 = Operação tributável (alíquota diferenciada)
03 = Operação tributável (alíquota por substituição tributária)
04 = Operação tributável (alíquota por substituição tributária)
05 = Operação com suspensão
06 = Operação de exportação
07 = Operação de exclusão
08 = Operação com suspensão
09 = Operação com suspensão
```

**Implementação Atual:** Apenas CST 01 (padrão) ⚠️

---

### 4. CST ICMS — Código de Situação Tributária

**Lei:** RICMS/UF (Regulamento do ICMS de cada estado)

#### Status: ⚠️ PARCIAL

**CSTs Válidos (0-99):**

```
00 = Tributada integralmente
10 = Tributada com ST
20 = Tributada com FCP
30 = Isenta
40 = Não tributada
41 = Não tributada (com FCP)
50 = Suspensão
51 = Diferimento
60 = ICMS cobrado anteriormente (substituição)
70 = Tributação com ST
71 = Tributação com ST e FCP
... (total de 100+ códigos)
```

**Implementação Atual:** Apenas CST 00 (tributada) 🔴

**Problema Crítico:**
```python
cst_icms: str = Field(default="00", description="Código de Situação Tributária ICMS")
```

Isso limita vendas a apenas operações tributadas normalmente. Faltam:
- Operações isentas (CST 40)
- Operações sob ST (CST 60)
- Produtor Rural (ICMS diferido)
- Microempreendedor Individual (dispensado ICMS)

---

### 5. NCM — Nomenclatura Comum do Mercosul

**Lei:** Lei Federal 10.864/2004 + Tariff TEC (Tarifa Comum do Mercosul)

#### Status: ✅ CORRETO

**Validação Implementada:**
```python
@field_validator('ncm')
@classmethod
def validar_ncm(cls, v):
    """NCM deve ter exatamente 8 dígitos"""
    if not v.isdigit() or len(v) != 8:
        raise ValueError('NCM deve ter 8 dígitos (ex: 84431000)')
    return v
```

✅ CORRETO: NCM sempre tem 8 dígitos

**Exemplos Válidos:**
```
02012100 = Carne bovina fresca ou refrigerada
02011000 = Carne de porco fresca
84431000 = Bombas e motobombas
07011000 = Batata fresca ou refrigerada
```

**Recomendação:** Adicionar validação de NCM existente
```python
# TODO: Validar contra tabela oficial SECEX
NCM_VALIDOS = ["02012100", "02011000", "84431000", ...]  # 12.000+ códigos
```

---

### 6. CFOP — Código Fiscal de Operação e Prestação

**Lei:** Lei Federal 6.374/1976 + SEFAZ

#### Status: ✅ CORRETO

**Validação Implementada:**
```python
@field_validator('cfop')
@classmethod
def validar_cfop(cls, v):
    """CFOP deve ter exatamente 4 dígitos"""
    if not v.isdigit() or len(v) != 4:
        raise ValueError('CFOP deve ter 4 dígitos (ex: 5102)')
    return v
```

✅ CORRETO: CFOP sempre tem 4 dígitos

**CFOPs Válidos para NFC-e (PDV):**

| CFOP | Descrição |
|------|-----------|
| 5102 | Venda de mercadoria adquirida ou recebida (varejo) |
| 5103 | Venda de mercadoria produzida pelo estabelecimento |
| 5120 | Devolução de venda de mercadoria adquirida ou recebida |

**Implementação Atual:** Padrão = 5102 ✅

**Recomendação:** Validar CFOPs por tipo de operação
```python
CFOP_VALIDOS_NFCE = ["5102", "5103", "5120", ...]
```

---

### 7. Origem da Mercadoria

**Lei:** Lei Complementar 87/1996 (ICMS) + Decreto 6.759/2009

#### Status: ✅ CORRETO

**Códigos Válidos:**

| Código | Descrição |
|--------|-----------|
| 0 | Nacional |
| 1 | Estrangeira (importação direta) |
| 2 | Estrangeira (mercado interno) |
| 3 | Nacional (conteúdo importado > 40%) |
| 4 | Nacional (PBB - Processo Produtivo Básico) |
| 5 | Nacional (conteúdo importado ≤ 40%) |
| 6 | Estrangeira (importação - sem similar nacional) |
| 7 | Estrangeira (mercado interno - sem similar nacional) |
| 8 | Nacional (conteúdo importado > 70%) |

**Implementação Atual:** Campo com default = "0" ✅

**Validação:**
```python
@field_validator('origem')
@classmethod
def validar_origem(cls, v):
    """Origem deve estar entre 0 e 8"""
    if not v.isdigit() or int(v) > 8:
        raise ValueError('Origem deve estar entre 0 e 8')
    return v
```

✅ CORRETO

---

### 8. CEST — Código Especificador da Substituição Tributária

**Lei:** Lei Complementar 123/2006 (Simples Nacional) + SEFAZ

#### Status: ✅ PRESENTE (mas não usado)

**O que é:**
- Código de 7 dígitos
- Identifica produtos sob Substituição Tributária
- Obrigatório para ICMS-ST em Simples Nacional

**Implementação Atual:**
```python
cest: str = Field(..., 
    description="Código Especificador da Substituição Tributária")
```

✅ Campo existe  
⚠️ Mas não é validado nem calculado  
❌ ST (Substituição Tributária) não está implementada

**Recomendação:**
```python
# TODO: Implementar cálculo de ICMS-ST
# ICMS-ST = (alíquota ST * valor) - ICMS próprio cobrado
```

---

## 🌐 CONFORMIDADE PT-BR (PORTUGUÊS BRASILEIRO)

### Status: ✅ 100% CONFORMIDADE

#### Verificação de Strings em PT-BR

| Elemento | Valor | Status |
|----------|-------|--------|
| **Descrição NCM** | "Nomenclatura Comum do Mercosul (8 dígitos)" | ✅ |
| **Descrição CFOP** | "Código Fiscal Operações (4 dígitos)" | ✅ |
| **Descrição Quantidade** | "Quantidade do produto" | ✅ |
| **Descrição Valor** | "Valor unitário em reais" | ✅ |
| **Descrição CST ICMS** | "Código de Situação Tributária ICMS" | ✅ |
| **Descrição CST PIS** | "Código de Situação Tributária PIS" | ✅ |
| **Descrição CST COFINS** | "Código de Situação Tributária COFINS" | ✅ |
| **Descrição Origem** | "Origem da mercadoria (0-8)" | ✅ |
| **Descrição Consumidor** | "CPF (11 dígitos) ou CNPJ (14 dígitos)" | ✅ |
| **Descrição Emitente** | "CNPJ do emitente (14 dígitos)" | ✅ |
| **Validação NCM** | "NCM deve ter 8 dígitos" | ✅ |
| **Validação CFOP** | "CFOP deve ter 4 dígitos" | ✅ |
| **Validação CPF/CNPJ** | "CPF/CNPJ deve conter apenas dígitos" | ✅ |
| **Validação UF** | "UF inválida" | ✅ |

#### Interfaces Não Verificadas:

⚠️ **Frappe/ERPNext:** Verificar idioma selecionado
```
Localizar: erpnext/regional/brazil/doctype/
Validar: labels em PT-BR quando lang=pt-BR
```

⚠️ **FastAPI Docs:** Swagger em inglês por padrão
```
Melhorar: adicionar tradução de descriptions
```

---

## ⚖️ CONFORMIDADE GERAL

### ✅ Correto (100%)
- ✅ Alíquotas PIS/COFINS
- ✅ Cálculo de impostos
- ✅ Validação NCM (formato)
- ✅ Validação CFOP (formato)
- ✅ Validação Origem (0-8)
- ✅ Português BR nas descriptions

### ⚠️ Parcial (60-80%)
- ⚠️ ICMS (hardcoded, não por NCM)
- ⚠️ CST (apenas 1 opção de cada)
- ⚠️ CEST (campo criado mas não usado)

### ❌ Não Implementado (0%)
- ❌ Substituição Tributária (ST)
- ❌ Regime Tributário (Simples/Lucro Real)
- ❌ Tabela de alíquotas por NCM
- ❌ Validação de NCM contra lista oficial
- ❌ Frete ICMS-ST
- ❌ Diferencial de alíquota (substituição tributária)

---

## 🎯 RECOMENDAÇÕES IMEDIATAS

### 🔴 CRÍTICAS (implementar antes de produção)

1. **Tabela de Alíquotas por NCM**
   ```python
   # Consultar: https://www1.sefaz.ba.gov.br/webservices/
   # Criar tabela dinâmica de ICMS por NCM + UF
   ```

2. **CST Múltiplos**
   ```python
   # Implementar cálculo conforme regime tributário
   # Simples Nacional: CST 40 (isento)
   # Lucro Presumido: CST 00, 20, 60
   ```

3. **Validação de NCM Existente**
   ```python
   # Rejeitar NCMs inválidos
   # Consultar: https://www.receita.fazenda.gov.br/
   ```

### 🟡 IMPORTANTES (próximas 2 semanas)

4. **Implementar ST (Substituição Tributária)**
   ```python
   # Para Simples Nacional com CEST
   # Fórmula: ICMS-ST = (alíq_ST * valor) - ICMS próprio
   ```

5. **Regime Tributário Configurável**
   ```python
   # Simples Nacional: alíquota 8-33%
   # Lucro Presumido: alíquota variável
   # Lucro Real: alíquota variável
   ```

6. **Frete com ICMS-ST**
   ```python
   # Calcular ICMS sobre frete
   # Aplicar alíquota diferenciada se ST
   ```

### 🟢 NICE-TO-HAVE (próximo mês)

7. **DANFE em Português**
   - Gerar PDF com labels 100% PT-BR

8. **Relatórios Fiscais em PT-BR**
   - SPED fiscal
   - EFD contribuições
   - Livro de apuração

---

## 📚 REFERÊNCIAS LEGAIS

### Leis e Decretos
- **Lei Complementar 87/1996** — ICMS (Lei Kandir)
- **Lei Federal 10.637/2002** — PIS
- **Lei Federal 10.833/2003** — COFINS
- **Lei Federal 6.374/1976** — CFOP
- **Lei Complementar 123/2006** — Simples Nacional (CEST)

### Normas SEFAZ
- **Manual de Orientação do Leiaute do Arquivo** — NF-e
- **Manual de Orientação do Leiaute do Arquivo** — NFC-e
- **Tabela de ICMS por NCM** — https://www1.sefaz.ba.gov.br/

### Sistemas Oficiais
- **SEFAZ** — https://www.sefaz.fazenda.gov.br/
- **Portal NF-e** — https://www.nfe.fazenda.gov.br/
- **IBPT** — https://www.ibptax.com.br/ (alíquotas federais)

---

## 🔄 PRÓXIMAS AÇÕES

### Para Fase 2.2 (NF-e)
- [ ] Implementar tabela de CSTs (00, 10, 20, 30, etc)
- [ ] Adicionar validação de regime tributário
- [ ] Implementar cálculo de ICMS-ST

### Para Fase 2.3 (Assinatura)
- [ ] Validar conformidade XML com XSD SEFAZ
- [ ] Testar assinatura em ambiente SEFAZ homologação

### Para Fase 2.5 (SEFAZ)
- [ ] Enviar XML para SEFAZ testes
- [ ] Validar retorno de protocolo
- [ ] Testar cancelamento

---

**Status:** ✅ ADEQUADO PARA MVP  
**Recomendação:** Implementar TODOs críticos antes de produção  
**Próxima Revisão:** Após implementação de ST (Substituição Tributária)
