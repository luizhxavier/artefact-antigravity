
from pathlib import Path

import pandas as pd


# 1. Localiza a pasta dos datasets
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# 2. Define os arquivos que vamos investigar
arquivos = {
    "CLIENTES": "desafio_tecnico_ai_eng - customers.csv",
    "PEDIDOS": "desafio_tecnico_ai_eng - orders.csv",
    "ITENS": "desafio_tecnico_ai_eng - order_items.csv"
}


# 3. Inspeciona a estrutura de cada arquivo
for nome, arquivo in arquivos.items():

    caminho = DATA_DIR / arquivo

    df = pd.read_csv(caminho)

    print(f"\n{'=' * 50}")
    print(f"DATASET: {nome}")
    print(f"LINHAS: {len(df)}")

    print("\nCOLUNAS E TIPOS:")
    print(df.dtypes)

    print("\nVALORES NULOS POR COLUNA:")
    print(df.isna().sum())

    # Mostra a distribuição de status, caso exista
    if "status" in df.columns:
        print("\nDISTRIBUIÇÃO DE STATUS:")
        print(df["status"].value_counts(dropna=False))
