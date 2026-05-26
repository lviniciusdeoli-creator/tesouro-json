"""
================================================
TESOURO DIRETO - CSV → JSON AUTOMÁTICO
================================================

Descrição:
1. Baixa automaticamente os CSVs do Tesouro Direto
2. Consolida os dados
3. Gera um único JSON estruturado

Arquivos utilizados:
- rendimento-resgatar-csv
- rendimento-investir-csv

================================================
DEPENDÊNCIAS
================================================

pip install pandas
pip install cloudscraper

================================================
"""

import pandas as pd
import json
import cloudscraper

from datetime import datetime

# ================================================
# CONFIGURAÇÕES
# ================================================

# URLS TESOURO DIRETO

url_resgatar = (
    "https://www.tesourodireto.com.br/"
    "documents/d/guest/rendimento-resgatar-csv?download=true"
)

url_investir = (
    "https://www.tesourodireto.com.br/"
    "documents/d/guest/rendimento-investir-csv?download=true"
)

# Arquivos temporários CSV

csv_resgatar = "rendimento-resgatar.csv"

csv_investir = "rendimento-investir.csv"

# Arquivo JSON final

json_file = "tesouro.json"

# ================================================
# CLOUDSCRAPER
# ================================================

scraper = cloudscraper.create_scraper(
    browser={
        "browser": "chrome",
        "platform": "windows",
        "mobile": False
    }
)

# ================================================
# DOWNLOAD CSV RESGATE
# ================================================

print("====================================")
print("Baixando CSV de RESGATE...")
print("====================================")

response = scraper.get(
    url_resgatar,
    timeout=30
)

response.raise_for_status()

with open(csv_resgatar, "wb") as f:

    f.write(response.content)

print("CSV RESGATE baixado com sucesso!")

# ================================================
# DOWNLOAD CSV INVESTIMENTO
# ================================================

print("====================================")
print("Baixando CSV de INVESTIMENTO...")
print("====================================")

response = scraper.get(
    url_investir,
    timeout=30
)

response.raise_for_status()

with open(csv_investir, "wb") as f:

    f.write(response.content)

print("CSV INVESTIMENTO baixado com sucesso!")

# ================================================
# LEITURA CSV RESGATE
# ================================================

df_resgate = pd.read_csv(
    csv_resgatar,
    sep=";",
    encoding="utf-8"
)

df_resgate.columns = df_resgate.columns.str.strip()

# ================================================
# RENOMEIA COLUNAS RESGATE
# ================================================

df_resgate.columns = [
    "titulo",
    "taxa_resgate",
    "preco_resgate",
    "vencimento"
]

# ================================================
# LEITURA CSV INVESTIMENTO
# ================================================

df_investir = pd.read_csv(
    csv_investir,
    sep=";",
    encoding="utf-8"
)

df_investir.columns = df_investir.columns.str.strip()

# ================================================
# REMOVE COLUNA INVESTIMENTO MÍNIMO
# ================================================

# Mantém apenas as colunas desejadas

df_investir = df_investir.iloc[:, [0,1,3,4]]

# ================================================
# RENOMEIA COLUNAS INVESTIMENTO
# ================================================

df_investir.columns = [
    "titulo",
    "taxa_compra",
    "preco_compra",
    "vencimento"
]

# ================================================
# IDENTIFICA TIPO
# ================================================

def identificar_tipo(titulo):

    titulo = titulo.upper()

    if "SELIC" in titulo:
        return "SELIC"

    elif any(
        termo in titulo
        for termo in ["IPCA", "EDUCA", "RENDA"]
    ):
        return "IPCA"

    elif "IGPM" in titulo:
        return "IGPM"

    elif "RESERVA" in titulo:
        return "SELIC"

    elif "PREFIXADO" in titulo:
        return "PREFIXADO"

    return "OUTRO"

# ================================================
# TRATAMENTO RESGATE
# ================================================

df_resgate["preco_resgate"] = (
    df_resgate["preco_resgate"]
    .astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df_resgate["preco_resgate"] = pd.to_numeric(
    df_resgate["preco_resgate"],
    errors="coerce"
)

df_resgate["taxa_resgate"] = (
    df_resgate["taxa_resgate"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

# ================================================
# TRATAMENTO INVESTIMENTO
# ================================================

df_investir["preco_compra"] = (
    df_investir["preco_compra"]
    .astype(str)
    .str.replace("R$", "", regex=False)
    .str.replace(".", "", regex=False)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

df_investir["preco_compra"] = pd.to_numeric(
    df_investir["preco_compra"],
    errors="coerce"
)

df_investir["taxa_compra"] = (
    df_investir["taxa_compra"]
    .astype(str)
    .str.replace(",", ".", regex=False)
    .str.strip()
)

# ================================================
# MERGE DOS DADOS
# ================================================

df_final = pd.merge(

    df_resgate,

    df_investir[[
        "titulo",
        "taxa_compra",
        "preco_compra"
    ]],

    on="titulo",

    how="outer"

)

# ================================================
# IDENTIFICA TIPO
# ================================================

df_final["tipo"] = (
    df_final["titulo"]
    .apply(identificar_tipo)
)

# ================================================
# TRATAMENTO DE VALORES AUSENTES
# ================================================

# Para títulos sem disponibilidade de investimento

df_final["preco_compra"] = (
    df_final["preco_compra"]
    .fillna("Não disponível para investimento")
)

df_final["taxa_compra"] = (
    df_final["taxa_compra"]
    .fillna("Não disponível para investimento")
)

# Remove demais NaN
df_final = df_final.where(
    pd.notnull(df_final),
    None
)

# ================================================
# CONVERTE PARA JSON
# ================================================

dados = df_final.to_dict(orient="records")

# ================================================
# DATA/HORA
# ================================================

agora = datetime.now()

atualizacao = agora.strftime(
    "%d/%m/%Y %H:%M:%S"
)

# ================================================
# ESTRUTURA FINAL
# ================================================

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

# ================================================
# FINALIZAÇÃO
# ================================================

print("====================================")
print("JSON criado com sucesso!")
print(f"Arquivo JSON: {json_file}")
print(f"Títulos processados: {len(dados)}")
print(f"Atualização: {atualizacao}")
print("====================================")
