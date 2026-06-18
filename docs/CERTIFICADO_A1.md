# 🔐 Guia de Provisioning - Certificado Digital A1

**Versão:** 1.0  
**Data:** 18/06/2026  
**Escopo:** Configuração de certificado digital para emissão de NF-e/NFC-e

---

## 📋 Índice

1. [O que é Certificado A1](#o-que-é-certificado-a1)
2. [Onde obter](#onde-obter)
3. [Tipos de Cartório](#tipos-de-cartório)
4. [Custos](#custos)
5. [Processo de aquisição](#processo-de-aquisição)
6. [Carregar no Docker](#carregar-no-docker)
7. [Teste com SEFAZ](#teste-com-sefaz)
8. [Troubleshooting](#troubleshooting)

---

## O que é Certificado A1?

**Certificado Digital A1** é um arquivo eletrônico criptografado (formato PFX ou P12) que identifica pessoa física ou jurídica perante órgãos fiscais.

### Características:

| Aspecto | Descrição |
|--------|-----------|
| **Formato** | PFX (PKCS#12) ou P12 |
| **Validade** | 1 ano (pessoa física) ou até 3 anos (pessoa jurídica) |
| **Armazenamento** | Arquivo + Senha |
| **Uso** | Assinatura digital de NF-e, NFC-e, EFD, e-LALUR |
| **Renovação** | Necessária após expiração |
| **Backup** | **CRÍTICO** - guardar cópia segura |

---

## Onde Obter

### 🇧🇷 Autoridades Certificadoras Brasileiras

As autoridades reconhecidas pelo ICP-Brasil (com foco em fiscal):

#### **1. Serasa Experian** (Recomendado)
- **Site:** https://www.serasaexperian.com.br/pf/certificados/
- **Certificados:** e-CNPJ, e-CPF, NF-e
- **Prazo:** 1-3 dias úteis
- **Custo:** ~R$150-300/ano (PJ)
- **Suporte:** Excelente
- **Cartório Online:** Sim

#### **2. Certisign**
- **Site:** https://www.certisign.com.br/
- **Certificados:** Similares à Serasa
- **Prazo:** 1-2 dias úteis
- **Custo:** ~R$180-280/ano
- **Suporte:** Bom
- **Cartório Online:** Sim

#### **3. Imprensa Oficial** (São Paulo)
- **Site:** https://www.imprensaoficial.com.br/
- **Certificados:** e-CNPJ, e-CPF
- **Prazo:** 2-5 dias úteis
- **Custo:** ~R$100-200/ano
- **Suporte:** Moderado
- **Cartório Online:** Parcial

#### **4. Notarize** (Nacional)
- **Site:** https://www.notarize.com.br/
- **Certificados:** Completo
- **Prazo:** 1-2 dias úteis
- **Custo:** ~R$150-250/ano
- **Suporte:** Bom
- **Cartório Online:** Sim (maioria dos estados)

---

## Tipos de Cartório

### 👤 **Para Pessoa Física (CPF)**
- Cartório de notas mais próximo
- Levar: RG, CPF, comprovante de residência
- Tempo no cartório: 30-60 minutos
- **Não precisa ir fisicamente** com Notarização Online

### 🏢 **Para Pessoa Jurídica (CNPJ)**
- Cartório de notas + Junta Comercial
- Levar: CNPJ, contrato social, RG do responsável
- Pode fazer **100% online** em alguns cartórios
- Tempo no cartório: 45-120 minutos (ou online 24h)

### 📱 **Online (Recomendado)**
- Não precisa sair de casa
- Válido legalmente (ICP-Brasil)
- Mais rápido (às vezes no mesmo dia)
- Video-chamada com notário

---

## Custos

### Pessoa Física (CPF)

| Autoridade | Taxa Cartório | Taxa AC | Total/ano |
|-----------|--------------|---------|----------|
| Serasa Experian | R$80-100 | R$80-150 | ~R$150-250 |
| Certisign | R$80-100 | R$80-150 | ~R$150-250 |
| Imprensa Oficial | R$60-80 | R$60-120 | ~R$100-200 |
| Notarize | R$80-100 | R$60-120 | ~R$150-220 |

### Pessoa Jurídica (CNPJ)

| Autoridade | Taxa Cartório | Taxa AC | Total/ano |
|-----------|--------------|---------|----------|
| Serasa Experian | R$100-150 | R$100-200 | ~R$200-350 |
| Certisign | R$100-150 | R$100-200 | ~R$200-350 |
| Imprensa Oficial | R$80-120 | R$80-150 | ~R$150-270 |
| Notarize | R$100-150 | R$80-150 | ~R$180-300 |

**Total anual:** ~R$150-350 (pessoa física) ou R$200-350 (pessoa jurídica)

---

## Processo de Aquisição

### **Opção A: Online (Recomendada) ⭐**

#### Passo 1: Escolher Autoridade
```bash
# Recomendação: Serasa ou Notarize
# Acessar site → Novo certificado → Escolher produto e-CNPJ/e-CPF
```

#### Passo 2: Preencher formulário
- [ ] CPF/CNPJ
- [ ] Email
- [ ] Telefone
- [ ] Dados de endereço
- [ ] Indicar para qual CNPJ (se PJ)

#### Passo 3: Videochamada com notário
- [ ] Agendar data/hora
- [ ] Ter documento de identidade à mão
- [ ] Estar em local tranquilo
- [ ] Assinar digitalmente os documentos
- **Duração:** 10-20 minutos

#### Passo 4: Gerar certificado
- [ ] AC gera arquivo PFX
- [ ] Enviar por email criptografado
- [ ] Fazer download seguro
- [ ] Guardar senha em local seguro
- **Tempo total:** 24-48 horas

---

### **Opção B: Presencialmente**

#### Passo 1: Agendar no Cartório
```bash
# Ligar ou acessar site do cartório mais próximo
# Agendar videonotarização ou presencial
```

#### Passo 2: Ir ao Cartório
- [ ] Levar documento original + CPF
- [ ] Apresentar-se ao tabelião
- [ ] Assinar documentos em papel
- **Duração:** 45-120 minutos

#### Passo 3: Ir na AC (ou online)
- [ ] AC envia instruções
- [ ] Fazer upload de documentação cópia
- [ ] Video-chamada se necessário
- Gerar PFX
- **Duração:** 1-2 dias

---

## Carregar no Docker

### **1. Preparar arquivo PFX**

```bash
# Você recebeu: certificado.pfx (ou .p12)
# Você recebeu: senha (guardar seguro!)

# Validar certificado (opcional):
openssl pkcs12 -info -in certificado.pfx -noout
# Vai pedir a senha
```

### **2. Copiar para container**

**Opção A: Montar como volume (Recomendado)**

Editar `docker-compose.yml`:

```yaml
services:
  erp-acbr:
    image: acbr:latest
    volumes:
      - ./certs:/app/certs:ro  # Certificados em read-only
    environment:
      CERT_PATH: /app/certs/certificado.pfx
      CERT_PASSWORD: ${CERT_PASSWORD}  # Usar .env
    ports:
      - "8080:8080"
```

Criar diretório:
```bash
mkdir -p certs/
cp /path/to/certificado.pfx certs/
chmod 400 certs/certificado.pfx  # Apenas leitura
```

**Opção B: Copiar no build (Menos seguro)**

```bash
# No Dockerfile do acbr-container:
COPY certs/certificado.pfx /app/certs/
RUN chmod 400 /app/certs/certificado.pfx
```

### **3. Configurar variáveis de ambiente**

Criar/editar `.env`:

```bash
# Certificado Digital
CERT_PATH=/app/certs/certificado.pfx
CERT_PASSWORD=sua_senha_super_secreta_aqui
CERT_VALID_FROM=2024-01-15  # Data de emissão
CERT_VALID_TO=2025-01-15    # Data de expiração

# SEFAZ
SEFAZ_ENVIRONMENT=testes  # ou 'producao'
SEFAZ_STATE=SP             # Estado padrão
```

### **4. Testar carregamento**

```bash
# Iniciar containers
docker-compose up -d

# Verificar logs
docker logs erp-acbr

# Testar endpoint de health
curl http://localhost:8080/health

# Resposta esperada:
# {
#   "status": "ok",
#   "certificado": "válido até 2025-01-15",
#   "erpbrasil": "3.1.1",
#   "sefaz": "pronto"
# }
```

---

## Teste com SEFAZ

### **1. Ambiente de Testes (Recomendado)**

A SEFAZ fornece ambiente de testes **100% gratuito**:

```bash
# Configurar em .env ou acbr-container/config/:
SEFAZ_ENVIRONMENT=testes
SEFAZ_WSDL=https://nfe.sefazrs.rs.gov.br/webservices/

# OU usar webservice homologação:
SEFAZ_URL=https://nfe.sefazrs.rs.gov.br/webservices/NFeAutorizacao4/NFeAutorizacao4.asmx
```

### **2. Solicitar acesso**

```bash
# 1. CNPJ precisa estar **ativo** na Receita Federal
# 2. Acessar: https://www.sefaz.fazenda.gov.br/
# 3. Clicar em "Empresas" → "NFe"
# 4. Fazer cadastro de usuário
# 5. Ativar contingência se necessário
```

### **3. Primeiro teste**

**Arquivo:** `acbr-container/tests/test_nfce_producao.py`

```python
import requests
import json

# Testar emissão de NFC-e com dados fictícios
payload = {
    "cnpj_emitente": "06117114000172",  # CNPJ válido
    "cpf_consumidor": "12345678901",    # CPF fictício (aceito em testes)
    "produtos": [
        {
            "ncm": "84431000",
            "descrição": "EQUIPAMENTO DE TESTE",
            "quantidade": 1,
            "valor_unitario": 100.00,
            "valor_total": 100.00,
            "icms_cst": "00",
            "icms_aliquota": 0.18,
        }
    ],
    "valor_total": 100.00,
}

response = requests.post(
    "http://localhost:8080/nfce/emitir",
    json=payload,
    timeout=30
)

print(json.dumps(response.json(), indent=2))
# Esperado: protocolo SEFAZ se sucesso
```

### **4. Validar resposta**

Se tudo funcionar:

```json
{
  "status": "sucesso",
  "chave_acesso": "35240618061171140001650010000000011234567890",
  "protocolo": "135240618061171140001650010000000011234567890",
  "xml_assinado": "<?xml version=\"1.0\"?>...",
  "qr_code": "https://www.sefaz.rs.gov.br/nfce/consultapublica/...",
  "timestamp": "2024-06-18T10:30:00Z"
}
```

---

## Troubleshooting

### ❌ Erro: "Certificado não encontrado"

```
SSLError: unable to get local issuer certificate
```

**Solução:**
```bash
# 1. Verificar path:
docker exec erp-acbr ls -la /app/certs/

# 2. Verificar permissões:
docker exec erp-acbr chmod 400 /app/certs/certificado.pfx

# 3. Validar certificado:
openssl pkcs12 -info -in certificado.pfx -noout
```

---

### ❌ Erro: "Senha do certificado inválida"

```
PKCS12 unable to parse structure: decryption failed
```

**Solução:**
```bash
# 1. Verificar se a senha está correta:
openssl pkcs12 -info -in certificado.pfx -passin pass:"SENHA_AQUI"

# 2. Tentar escape de caracteres especiais:
# Se senha tem $ # @ &, usar aspas:
export CERT_PASSWORD='$en@#a!'

# 3. Se ainda não funcionar, re-gerar no cartório
```

---

### ❌ Erro: "Certificado expirado"

```
ValueError: Certificado expirado em 2025-01-15
```

**Solução:**
```bash
# 1. Verificar data de expiração:
openssl pkcs12 -info -in certificado.pfx -noout | grep notAfter

# 2. Renovar no cartório (30 dias antes de expirar)
# 3. Carregar novo arquivo
```

---

### ❌ Erro: "SEFAZ rejeitou assinatura"

```
SOAP Fault: Assinatura não válida para NFe
```

**Solução:**
```bash
# 1. Verificar se certificado é realmente NF-e:
openssl pkcs12 -nokeys -in certificado.pfx | grep -i nfe

# 2. Verificar SE certificado está para o CNPJ correto:
openssl pkcs12 -nokeys -in certificado.pfx | grep subject

# 3. Testar em ambiente SEFAZ de testes antes de produção
# 4. Contatar suporte do cartório se problema persistir
```

---

### ⚠️ Erro: "Contingência SEFAZ"

```
SEFAZ momentaneamente indisponível
```

**Solução:**
```bash
# SEFAZ entra em contingência periodicamente
# Opções:
# 1. Usar NFC-e em contingência (PDF assinado)
# 2. Usar formulário impresso
# 3. Aguardar restabelecimento (geralmente <2 horas)
# 4. Avisar cliente: "Sistema fora do ar temporariamente"

# Para NFC-e contingência:
curl -X POST http://localhost:8080/nfce/gerar-pdf-contingencia \
  -H "Content-Type: application/json" \
  -d @payload.json
```

---

### ✅ Sucesso!

Se conseguiu gerar NFC-e com sucesso:

```bash
# 1. Testar em produção
# 2. Guardar backup do certificado em local seguro (pendrive criptografado)
# 3. Renovar antes da expiração
# 4. Monitorar logs para erros de assinatura
```

---

## 📚 Referências

- **ICP-Brasil:** https://www.gov.br/iti/pt-br/assuntos/acp-autoridade-certificadora-da-presidencia
- **SEFAZ RS:** https://www.sefaz.rs.gov.br/ (principal webservice NFe)
- **Manual NFe:** http://www.nfe.fazenda.gov.br/
- **erpbrasil.edoc:** https://github.com/harenson/erpbrasil.edoc

---

**Última atualização:** 18/06/2026  
**Próxima revisão:** Quando ICP-Brasil publicar novas regras
