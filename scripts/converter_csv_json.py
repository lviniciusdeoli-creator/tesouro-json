"""
================================================
TESOURO DIRETO CSV → JSON CONVERTER
================================================

Descrição:
Converte o arquivo CSV do Tesouro Direto
para um arquivo JSON estruturado.

Objetivo:
Permitir integração simples com:

- Google Sheets
- Google Apps Script
- Power BI
- Python
- Dashboards financeiros

================================================
ESTRUTURA ESPERADA
================================================

/
├── tesouro.json
│
├── scripts/
│   └── converter_csv_json.py

================================================
"""

import pandas as pd
import json
from datetime import datetime

# ================================================
# CONFIGURAÇÕES
# ================================================

# Nome do CSV de entrada
csv_file = "../rendimento-resgatar.csv"

# Nome do JSON de saída
json_file = "../tesouro.json"

# ================================================
# LEITURA CSV
# ================================================

df = pd.read_csv(
    csv_file,
    sep=";",
    encoding="utf-8"
)

# Remove espaços extras
df.columns = df.columns.str.strip()

# ================================================
# RENOMEIA COLUNAS
# ================================================

df.columns = [
    "titulo",
    "rendimento_anual",
    "preco_resgate",
    "vencimento"
]

# ================================================
# IDENTIFICA TIPO DO TÍTULO
# ================================================

def identificar_tipo(titulo):

    titulo = titulo.upper()

    if "SELIC" in titulo:
        return "SELIC"

    elif "IPCA" in titulo:
        return "IPCA"

    elif "PREFIXADO" in titulo:
        return "PREFIXADO"

    return "OUTRO"

df["tipo"] = df["titulo"].apply(identificar_tipo)

# ================================================
# TRATAMENTO DOS DADOS
# ================================================

# Remove símbolo R$
df["preco_resgate"] = (
    df["preco_resgate"]
    .astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

# Converte para número
df["preco_resgate"] = pd.to_numeric(
    df["preco_resgate"],
    errors="coerce"
)

# Padroniza rendimento
df["rendimento_anual"] = (
    df["rendimento_anual"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

# Remove valores nulos
df = df.where(pd.notnull(df), None)

# ================================================
# CONVERTE PARA JSON
# ================================================

dados = df.to_dict(orient="records")

# Data e hora atual
agora = datetime.now()

atualizacao = agora.strftime("%d/%m/%Y %H:%M:%S")

# Estrutura final do JSON
estrutura = {
    "fonte": "Tesouro Direto",
    "quantidade_titulos": len(dados),
    "atualizacao": atualizacao,
    "titulos": dados
}

# ================================================
# SALVA JSON
# ================================================

with open(json_file, "w", encoding="utf-8") as f:

    json.dump(
        estrutura,
        f,
        ensure_ascii=False,
        indent=4
    )

print("====================================")
print("JSON criado com sucesso!")
print(f"Arquivo gerado: {json_file}")
print(f"Títulos processados: {len(dados)}")
print(f"Atualização: {atualizacao}")
print("====================================")
