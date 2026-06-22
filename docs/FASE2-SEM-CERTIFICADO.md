# 🚀 FASE 2 — O QUE FAZER SEM CERTIFICADO DIGITAL A1

**Situação:** Temos código pronto, falta certificado para assinar e enviar SEFAZ  
**Solução:** Implementar 80% da Fase 2 AGORA (sem assinatura/SEFAZ)

---

## 📊 MATRIZ: O QUE PRECISA / NÃO PRECISA DE CERTIFICADO

```
TAREFAS FASE 2:

🟢 PODE FAZER JÁ (não precisa certificado)
  ├─ 2.1 ✅ Geração XML NFC-e (PRONTO)
  ├─ 2.2 ✅ Geração XML NF-e (similar à 2.1)
  ├─ 2.4 ✅ Geração QR Code
  ├─ 2.6 ✅ Formatação de DANFE PDF
  ├─ 2.7 ✅ Impressão de cupom
  ├─ 2.8 ✅ Tabelas fiscais (NCM, CFOP, ICMS)
  └─ 2.9 ✅ Validações fiscais completas

🔴 PRECISA CERTIFICADO (aguardar)
  ├─ 2.3 ❌ Assinatura digital XML
  └─ 2.5 ❌ Envio para SEFAZ webservice

⚙️ PODE PREPARAR (mock/teste)
  ├─ 2.3 Mock ➜ Simular assinatura
  └─ 2.5 Mock ➜ Simular resposta SEFAZ
```

---

## 🎯 PLANO DE AÇÃO: 10 TAREFAS SEM CERTIFICADO

### **TAREFA 2.1.1: Corrigir Conformidade Fiscal ⏱️ 2 DIAS**

**O que fazer:**
```python
# Implementar tabela dinâmica de ICMS por NCM
ICMS_ALIQUOTA_POR_NCM = {
    "02012100": 12.0,   # Carne bovina (alimento)
    "02011000": 12.0,   # Carne porco (alimento)
    "07011000": 12.0,   # Batata (alimento)
    "84431000": 18.0,   # Equipamentos
    # ... 10.000+ códigos
}

# Implementar CST múltiplos
CST_ICMS = {
    "00": "Tributada integralmente",
    "20": "Tributada com FCP",
    "40": "Não tributada",
    "60": "ICMS anterior (ST)",
}

# Implementar regime tributário
REGIME_TRIBUTARIO = {
    "SN": "Simples Nacional",
    "LR": "Lucro Real",
    "LP": "Lucro Presumido",
}
```

**Benefício:** Conformidade fiscal 100%  
**Dependência:** Nenhuma (apenas código)  
**Teste:** Unitários sim, SEFAZ depois

---

### **TAREFA 2.2: Geração XML NF-e ⏱️ 3 DIAS**

**O que fazer:**
```python
# Copiar estrutura de nfce_generator.py
# Adaptar para NF-e (mais campos):
├─ Múltiplos produtos (não só 1)
├─ Destinatário obrigatório
├─ Frete e seguro
├─ ICMS-ST (Substituição Tributária)
├─ Desconto/Acréscimo
├─ Transportador
└─ Cálculos mais complexos
```

**Arquivo:** `acbr-container/api/nfe_generator.py` (novo)  
**Testes:** `test_nfe_generator.py` (novo - 20+ testes)  
**Não precisa:** Certificado, SEFAZ

**Status:** XML funcional, sem assinatura

---

### **TAREFA 2.4: Geração de QR Code ⏱️ 1 DIA**

**O que fazer:**
```python
# QR Code conforme SEFAZ NFC-e
# Conteúdo:
#  35 (UF) | 06117114000172 (CNPJ) | 65 (MOD) | 1 (SERIE)
#  | 00000001 (NUMERO) | 100.00 (VALOR) | 12345678901 (CPF)
#  | 2024-06-18 (DATA) | 14:30:00 (HORA) | ASSINATURA

import qrcode

class QrcodeGenerator:
    def gerar_qrcode_nfce(self, chave: str, valor: str) -> bytes:
        """Retorna QR Code em PNG"""
        conteudo = f"https://www.sefaz.rs.gov.br/nfce/consultapublica/?..."
        qr = qrcode.QRCode()
        qr.add_data(conteudo)
        qr.make()
        img = qr.make_image()
        return img.tobytes()
```

**Não precisa:** Certificado, assinatura, SEFAZ  
**Pode testar:** Ler QR com celular

---

### **TAREFA 2.6: Formatação DANFE em PDF ⏱️ 3 DIAS**

**O que fazer:**
```python
# DANFE = Documento Auxiliar Nota Fiscal Eletrônica
# Usar ReportLab (já nos requirements)

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

class DanfeGenerator:
    def gerar_danfe_nfc_e(self, xml: str) -> bytes:
        """Gera PDF do cupom NFC-e (formato 80mm)"""
        # Cabeçalho: CNPJ, Nome, Endereço
        # Produtos: NCM, Descrição, Qtd, Valor, Total
        # Impostos: ICMS, PIS, COFINS
        # QR Code (imagem)
        # Rodapé: Chave de acesso, Protocolo (quando assinar)
        
        pdf = canvas.Canvas(...)
        # ... desenhar DANFE
        return pdf.getvalue()
```

**Não precisa:** Certificado  
**Pode testar:** Abrir PDF no navegador

---

### **TAREFA 2.7: Impressão em Impressora Térmica ⏱️ 2 DIAS**

**O que fazer:**
```python
# Usar CUPS (já está no container)
import cups

class ImpressoraTermica:
    def imprimir_cupom(self, pdf: bytes, impressora="TM-T20"):
        """Imprime cupom em impressora 80mm"""
        conn = cups.Connection()
        conn.printFile(
            "TM-T20",  # nome da impressora
            "cupom.pdf",
            title="NFC-e",
        )
```

**Não precisa:** Certificado  
**Pode testar:** Em PDV real (se tiver impressora)

---

### **TAREFA 2.8: Tabelas Fiscais (NCM, CFOP) ⏱️ 2 DIAS**

**O que fazer:**
```python
# 1. Popular tabelas NCM (12.000+ códigos)
#    Fonte: https://www.receita.fazenda.gov.br/

# 2. Popular tabelas CFOP (100+ códigos)
CFOP_TABELA = {
    "5102": "Venda de mercadoria adquirida ou recebida (varejo)",
    "5103": "Venda de mercadoria produzida pelo estabelecimento",
    "5120": "Devolução de venda de mercadoria adquirida",
    # ... 50+ códigos
}

# 3. Criar endpoints para consulta
@app.get("/ncm/{codigo}")
async def consultar_ncm(codigo: str):
    """Retorna descrição e alíquota do NCM"""
    return {
        "ncm": "02012100",
        "descricao": "Carne bovina fresca",
        "aliquota_icms": 12.0,
    }

@app.get("/cfop/{codigo}")
async def consultar_cfop(codigo: str):
    """Retorna descrição do CFOP"""
    return {
        "cfop": "5102",
        "descricao": "Venda varejo",
    }
```

**Não precisa:** Certificado  
**Pode testar:** Chamar endpoints

---

### **TAREFA 2.9: Validações Fiscais Completas ⏱️ 1 DIA**

**O que fazer:**
```python
# Adicionar validadores de negócio (além de Pydantic)

class ValidadoresFiscais:
    def validar_nfce_completa(self, payload: NfcePayload) -> list[str]:
        """Retorna lista de erros (vazio = válido)"""
        erros = []
        
        # Validar NCM existente
        if not self.ncm_existe(payload.produtos[0].ncm):
            erros.append(f"NCM {ncm} não existe")
        
        # Validar CFOP para tipo de operação
        if not self.cfop_valido_para_tipo(cfop, "venda"):
            erros.append(f"CFOP {cfop} inválido para venda")
        
        # Validar alíquota ICMS por NCM
        aliquota = self.obter_aliquota_icms(ncm, uf)
        if payload.aliquota_icms != aliquota:
            erros.append(f"ICMS deveria ser {aliquota}%, não {payload.aliquota_icms}%")
        
        # Validar ST se Simples Nacional com CEST
        if self.regime_sn and payload.cest and not payload.icms_st:
            erros.append("Simples Nacional com CEST requer ST calculado")
        
        return erros
```

**Não precisa:** Certificado  
**Pode testar:** Rodar validações

---

### **TAREFA 2.3 Mock: Simular Assinatura ⏱️ 1 DIA**

**O que fazer:**
```python
# Criar assinador mock (não assina de verdade, mas simula)

class AssinadorMock:
    def assinar_xml(self, xml: str) -> str:
        """Simula assinatura (para testes)"""
        # Em produção: usar signxml + certificado real
        # Aqui: apenas adiciona tag <Signature> fake
        
        xml_assinado = xml.replace(
            "</infNFe>",
            """
            <Signature>
                <SignatureValue>MOCK_SIGNATURE_VALUE_12345</SignatureValue>
            </Signature>
            </infNFe>
            """
        )
        return xml_assinado
```

**Benefício:** Testar fluxo completo sem certificado  
**Depois:** Trocar por `AssinadorReal` quando tiver certificado

---

### **TAREFA 2.5 Mock: Simular SEFAZ ⏱️ 1 DIA**

**O que fazer:**
```python
# Criar cliente SEFAZ mock (não envia de verdade)

class SefazClientMock:
    def transmitir_nfce(self, xml_assinado: str) -> dict:
        """Simula resposta SEFAZ"""
        return {
            "status": "sucesso",
            "protocolo": "135240618061171140001650010000000011234567890",
            "chave_acesso": "35240618061171140001650010000000011234567890",
            "data_autorizacao": "2024-06-18T14:30:00",
            "xml_processado": xml_assinado,
        }
```

**Benefício:** Testar integração Frappe → ACBr → SEFAZ  
**Depois:** Trocar por `SefazClientReal` quando tiver certificado

---

## 📈 TIMELINE SEM CERTIFICADO

```
HOJE (18/06):
  └─ ✅ Fase 2.1 XML NFC-e (PRONTO)

PRÓXIMOS 7 DIAS:
  ├─ 📝 Dia 1: Tarefa 2.1.1 (Conformidade fiscal)
  ├─ 📝 Dia 2-3: Tarefa 2.2 (XML NF-e)
  ├─ 📝 Dia 4: Tarefa 2.4 (QR Code)
  ├─ 📝 Dia 5: Tarefa 2.6 (DANFE PDF)
  ├─ 📝 Dia 6: Tarefa 2.7 (Impressão térmica)
  ├─ 📝 Dia 7: Tarefa 2.8 (Tabelas fiscais)
  └─ ✅ Fim de semana: Tarefa 2.9 (Validações)

SEMANA 2 (com Mock):
  ├─ 📝 Dia 8: Tarefa 2.3 Mock (simular assinatura)
  ├─ 📝 Dia 9: Tarefa 2.5 Mock (simular SEFAZ)
  └─ 🧪 Dia 10: Testes E2E (fluxo completo)

SEMANA 3 (QUANDO TIVER CERTIFICADO):
  ├─ 🔑 Trocar AssinadorMock por AssinadorReal
  ├─ 🔑 Trocar SefazClientMock por SefazClientReal
  ├─ 🧪 Testar em SEFAZ homologação
  └─ ✅ Ativar em produção
```

---

## 📊 COBERTURA SEM CERTIFICADO

```
O QUE FUNCIONA (100%):

✅ Geração XML NFC-e e NF-e
   ├─ Estrutura SEFAZ layout 4.0
   ├─ Validação de entrada
   ├─ Cálculos de impostos
   └─ Chave de acesso

✅ QR Code
   └─ Código 2D válido conforme SEFAZ

✅ DANFE em PDF
   └─ Documento para impressão/tela

✅ Impressão Térmica
   └─ Integração com impressora 80mm

✅ Tabelas Fiscais
   ├─ NCM (classificação)
   ├─ CFOP (tipo de operação)
   ├─ Alíquotas ICMS por NCM/UF
   └─ CST múltiplos

✅ Validações Fiscais
   ├─ NCM válido?
   ├─ CFOP válido para tipo?
   ├─ Alíquota correta?
   ├─ Regime tributário correto?
   └─ ST obrigatório?

✅ Testes Unitários
   └─ 100+ testes do fluxo

✅ Testes E2E (com mock)
   └─ Simular venda completa até cupom
```

```
O QUE NÃO FUNCIONA (precisa certificado):

❌ Assinatura Digital
   └─ Requer certificado A1

❌ Transmissão SEFAZ Real
   └─ Requer assinatura + SEFAZ online

❌ Protocolo Real
   └─ Só SEFAZ retorna
```

---

## 💡 ESTRATÉGIA: MVP SEM CERTIFICADO

### Fase A: Preparação (7 dias)
```
Implementar tudo EXCETO assinatura/SEFAZ
Resultado: Sistema 100% pronto para funcionamento
           Só falta "conectar" com SEFAZ
```

### Fase B: Certificado Chegar (N dias)
```
Ao receber certificado A1:
  1. Implementar AssinadorReal (2 horas)
  2. Implementar SefazClientReal (2 horas)
  3. Testar em SEFAZ homologação (2 horas)
  4. Ativar em produção (1 hora)
  
Total: 7 horas = menos de 1 dia!
```

---

## 🎯 RECOMENDAÇÃO

**Fazemos SIM:**
1. ✅ Implementar 9 tarefas (80% da Fase 2)
2. ✅ Criar testes completos (com mock)
3. ✅ Testar PDV em local
4. ✅ Treinar equipe

**Quando certificado chegar:**
1. 🔑 Ativar assinatura real (< 1 dia)
2. 🔑 Testar SEFAZ homologação (< 1 dia)
3. 🔑 Deploy produção (< 1 dia)

**Resultado Final:** Sistema pronto em **8-10 dias** (vs 15 se esperar certificado)

---

## 📋 CHECKLIST: COMEÇAMOS HOJE?

- [ ] Tarefa 2.1.1 (Conformidade fiscal) — 2 dias
- [ ] Tarefa 2.2 (NF-e) — 3 dias
- [ ] Tarefa 2.4 (QR Code) — 1 dia
- [ ] Tarefa 2.6 (DANFE) — 3 dias
- [ ] Tarefa 2.7 (Impressão) — 2 dias
- [ ] Tarefa 2.8 (Tabelas) — 2 dias
- [ ] Tarefa 2.9 (Validações) — 1 dia
- [ ] Tarefa 2.3 Mock — 1 dia
- [ ] Tarefa 2.5 Mock — 1 dia
- [ ] Testes E2E — 2 dias

**Total: 18 dias** (sem pressa)

---

**Você quer que começamos?** 🚀
