
from decimal import Decimal, ROUND_HALF_UP

import pytest

from src.catalogo import catalogo
from src.promocoes import calcular_preco_final, promocoes


# Testa os quatro produtos em promoção
@pytest.mark.parametrize(
    "product_id, preco_esperado, desconto",
    [
        (127, 323.10, 10),
        (121, 439.20, 20),
        (90, 1967.18, 18),
        (94, 5519.08, 8),
    ]
)
def test_promocoes_ativas(
    product_id,
    preco_esperado,
    desconto
):
    resultado = calcular_preco_final(
        product_id=product_id,
        pagamento_pix=True
    )

    assert resultado["tipo_desconto"] == "promocao"

    assert resultado["percentual_desconto"] == desconto

    assert resultado["preco_final_brl"] == pytest.approx(
        preco_esperado
    )

    assert resultado["desconto_pix_acumulado"] is False


# Verifica o PIX em um produto sem promoção ativa
def test_pix_sem_promocao():

    ids_promocionais = promocoes.loc[
        promocoes["is_active"] == 1,
        "product_id"
    ]

    produtos_elegiveis = catalogo.loc[
        (catalogo["status"] == "active")
        & (catalogo["stock_quantity"] > 0)
        & (~catalogo["product_id"].isin(ids_promocionais))
    ]

    assert not produtos_elegiveis.empty

    product_id = int(
        produtos_elegiveis.iloc[0]["product_id"]
    )

    resultado = calcular_preco_final(
        product_id=product_id,
        pagamento_pix=True
    )

    preco_original = Decimal(
        str(resultado["preco_tabela_brl"])
    )

    preco_esperado = (
        preco_original * Decimal("0.95")
    ).quantize(
        Decimal("0.01"),
        rounding=ROUND_HALF_UP
    )

    assert resultado["tipo_desconto"] == "pix"

    assert Decimal(
        str(resultado["preco_final_brl"])
    ) == preco_esperado


# Verifica produtos inexistentes
def test_produto_inexistente():

    resultado = calcular_preco_final(
        product_id=999999,
        pagamento_pix=True
    )

    assert resultado["erro"] == "Produto não encontrado."


# Verifica produtos indisponíveis
def test_produto_indisponivel():

    indisponiveis = catalogo.loc[
        (catalogo["status"] != "active")
        | (catalogo["stock_quantity"] <= 0)
    ]

    assert not indisponiveis.empty

    product_id = int(
        indisponiveis.iloc[0]["product_id"]
    )

    resultado = calcular_preco_final(
        product_id=product_id
    )

    assert resultado["erro"] == "Produto indisponível para venda."
