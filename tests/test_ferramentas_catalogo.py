
import pytest

from src.ferramentas_catalogo import consultar_catalogo


def test_ukuleles_promocionais_sem_acumular_pix():

    resultado = consultar_catalogo(
        categoria="ukulele",
        preco_maximo=500,
        pagamento_pix=True
    )

    produtos = {
        produto["product_id"]: produto
        for produto in resultado["produtos"]
    }

    # Kalani: promoção de 10%, sem acumular PIX
    assert produtos[127]["tipo_desconto"] == "promocao"
    assert produtos[127]["percentual_desconto"] == 10
    assert produtos[127]["preco_final_brl"] == pytest.approx(323.10)

    # Ohana: promoção de 20%, sem acumular PIX
    assert produtos[121]["tipo_desconto"] == "promocao"
    assert produtos[121]["percentual_desconto"] == 20
    assert produtos[121]["preco_final_brl"] == pytest.approx(439.20)


def test_orcamento_considera_preco_com_desconto():

    resultado = consultar_catalogo(
        categoria="ukulele",
        preco_maximo=330,
        pagamento_pix=True
    )

    ids = [
        produto["product_id"]
        for produto in resultado["produtos"]
    ]

    # O Kalani custa R$ 359 de tabela,
    # mas entra no orçamento com a promoção de R$ 323,10.
    assert 127 in ids

    assert all(
        produto["preco_final_brl"] <= 330
        for produto in resultado["produtos"]
    )


def test_produtos_sem_promocao_recebem_pix():

    resultado = consultar_catalogo(
        categoria="ukulele",
        preco_maximo=500,
        pagamento_pix=True
    )

    produtos_pix = [
        produto
        for produto in resultado["produtos"]
        if produto["tipo_desconto"] == "pix"
    ]

    assert len(produtos_pix) > 0

    assert all(
        produto["percentual_desconto"] == 5
        for produto in produtos_pix
    )
