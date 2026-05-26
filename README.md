# Tesouro Direto JSON API

Este repositório disponibiliza um arquivo JSON estruturado contendo informações atualizadas dos títulos públicos do Tesouro Direto.

O principal objetivo deste projeto é facilitar a integração dos dados do Tesouro Direto com:

- Google Sheets
- Google Apps Script
- Power BI
- Python
- Dashboards financeiros
- APIs próprias
- Estudos e automações financeiras

---

# Objetivo

O Tesouro Direto disponibiliza os dados originalmente em formato CSV.

Este projeto converte esses dados para JSON estruturado, permitindo um consumo muito mais simples em aplicações e planilhas.

A principal utilização deste repositório é permitir que planilhas do Google Sheets importem automaticamente os dados dos títulos públicos por meio de Google Apps Script.

---

# Estrutura do JSON

O arquivo contém:

- Fonte dos dados
- Quantidade de títulos disponíveis
- Data e hora da última atualização
- Lista completa dos títulos públicos

Cada título contém:

- Nome do título
- Tipo do título
- Rentabilidade anual
- Preço unitário de resgate
- Data de vencimento

---

# Exemplo de estrutura

```json
{
    "fonte": "Tesouro Direto",
    "quantidade_titulos": 61,
    "atualizacao": "26/05/2026 03:54:08",
    "titulos": [
        {
            "titulo": "Tesouro Educa+ 2027",
            "taxa_resgate": "IPCA + 7.97%",
            "preco_resgate": 3744.87,
            "vencimento": "15/12/2031",
            "taxa_compra": "IPCA + 7.85%",
            "preco_compra": 37.57,
            "tipo": "OUTRO"
        }
    ]
}
```

---

# Tipos de títulos disponíveis

O JSON contempla atualmente:

- Tesouro Selic
- Tesouro Prefixado
- Tesouro IPCA+
- Tesouro Renda+
- Tesouro Educa+
- Tesouro IGPM+
- Outros títulos públicos disponíveis

---

# Utilização no Google Sheets

Exemplo básico utilizando Google Apps Script:

```javascript
function importarTesouro() {

  const url =
    "LINK_RAW_DO_JSON";

  const response = UrlFetchApp.fetch(url);

  const dados = JSON.parse(response.getContentText());

  Logger.log(dados.atualizacao);

}
```

---

# Atualização dos dados

Os dados podem ser atualizados periodicamente através de scripts em Python responsáveis por:

1. Baixar o CSV original do Tesouro Direto
2. Converter os dados para JSON
3. Atualizar automaticamente este repositório

---

# Finalidade do projeto

Este projeto foi criado com foco em:

- Automatização financeira
- Integração com Google Sheets
- Estudos sobre renda fixa
- Consolidação de dados do Tesouro Direto
- Desenvolvimento de dashboards financeiros
- Criação de APIs financeiras simples

---

# Fonte dos dados

Os dados originais pertencem ao Tesouro Direto:

https://www.tesourodireto.com.br

---

# Licença

Este projeto possui finalidade educacional e de automação de dados financeiros públicos.
