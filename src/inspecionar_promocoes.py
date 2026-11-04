
from pathlib import Path
import pandas as pd


# 1. Localiza a pasta de dados
DATA_DIR = Path(__file__).resolve().parent.parent / "data"


# 2. Carrega os arquivos
promocoes = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - promotions.csv"
)

produtos = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - products.csv"
)


# 3. Verifica a distribuição de promoções ativas e inativas
print("\nSITUAÇÃO DAS PROMOÇÕES:")
print(promocoes["is_active"].value_counts(dropna=False))


# 4. Seleciona apenas as promoções ativas
promocoes_ativas = promocoes.loc[
    promocoes["is_active"] == 1
].copy()

print(f"\nTotal de promoções ativas: {len(promocoes_ativas)}")


# 5. Junta as promoções ativas aos produtos
resultado = promocoes_ativas.merge(
    produtos[
        [
            "product_id",
            "name",
            "price_brl",
            "stock_quantity",
            "status"
        ]
    ],
    on="product_id",
    how="left",
    validate="many_to_one",
    indicator=True
)


# 6. Mostra os produtos com promoções ativas
print("\nPRODUTOS COM PROMOÇÕES ATIVAS:")

if resultado.empty:
    print("Nenhuma promoção ativa encontrada.")
else:
    print(
        resultado[
            [
                "promotion_id",
                "product_id",
                "name",
                "price_brl",
                "discount_percent",
                "description",
                "stock_quantity",
                "status",
                "_merge"
            ]
        ].to_string(index=False)
    )
