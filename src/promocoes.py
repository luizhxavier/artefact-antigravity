
from pathlib import Path
from decimal import Decimal, ROUND_HALF_UP

import pandas as pd

from src.catalogo import catalogo


# =========================================================
# 1. CARREGAMENTO DAS PROMOÇÕES
# =========================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

promocoes = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - promotions.csv"
)


# =========================================================
# 2. CÁLCULO DO PREÇO FINAL
# =========================================================

def calcular_preco_final(
    product_id: int,
    pagamento_pix: bool = False
) -> dict:
    """
    Calcula o preço final de um instrumento musical.

    Args:
        product_id: Identificador do produto no catálogo.
        pagamento_pix: Indica se o cliente deseja pagar via PIX.

    Regras:
        - Promoções ativas têm prioridade.
        - O desconto PIX é de 5% quando não há promoção.
        - Os descontos não são cumulativos.
    """

    # Procura o produto no catálogo
    produtos_encontrados = catalogo.loc[
        catalogo["product_id"] == product_id
    ]

    if produtos_encontrados.empty:
        return {
            "product_id": product_id,
            "erro": "Produto não encontrado."
        }

    produto = produtos_encontrados.iloc[0]

    # Confirma se o produto pode ser vendido
    if (
        produto["status"] != "active"
        or produto["stock_quantity"] <= 0
    ):
        return {
            "product_id": product_id,
            "nome": produto["name"],
            "erro": "Produto indisponível para venda."
        }

    # Procura promoções ativas desse produto
    promocoes_produto = promocoes.loc[
        (promocoes["product_id"] == product_id)
        & (promocoes["is_active"] == 1)
    ]

    # Evita escolher arbitrariamente entre promoções
    if len(promocoes_produto) > 1:
        raise ValueError(
            f"Produto {product_id} possui múltiplas "
            "promoções ativas. É necessária uma regra "
            "de prioridade."
        )

    # Usa Decimal para calcular valores monetários
    preco_tabela = Decimal(str(produto["price_brl"]))

    if not promocoes_produto.empty:

        promocao = promocoes_produto.iloc[0]

        percentual = int(promocao["discount_percent"])
        tipo_desconto = "promocao"
        descricao = str(promocao["description"])

    elif pagamento_pix:

        percentual = 5
        tipo_desconto = "pix"
        descricao = "Desconto para pagamento via PIX"

    else:

        percentual = 0
        tipo_desconto = "nenhum"
        descricao = "Preço de tabela"

    # Aplica somente o desconto escolhido
    fator = Decimal(100 - percentual) / Decimal(100)

    preco_final = (
        preco_tabela * fator
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    return {
        "product_id": product_id,
        "nome": produto["name"],
        "preco_tabela_brl": float(preco_tabela),
        "percentual_desconto": percentual,
        "tipo_desconto": tipo_desconto,
        "descricao": descricao,
        "preco_final_brl": float(preco_final),
        "desconto_pix_acumulado": False
    }


# =========================================================
# 3. TESTES MANUAIS
# =========================================================

if __name__ == "__main__":

    ids_promocionais = [127, 121, 90, 94]

    for product_id in ids_promocionais:

        resultado = calcular_preco_final(
            product_id=product_id,
            pagamento_pix=True
        )

        print("\nPRODUTO:", resultado["nome"])
        print("PREÇO ORIGINAL:", resultado["preco_tabela_brl"])
        print("DESCONTO:", resultado["percentual_desconto"])
        print("TIPO:", resultado["tipo_desconto"])
        print("PREÇO FINAL:", resultado["preco_final_brl"])
