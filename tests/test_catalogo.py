
from src.catalogo import buscar_produtos


def test_buscar_violoes():
    resultado = buscar_produtos("Violões", 1000)

    assert not resultado.empty
    assert len(resultado) == 12


def test_normalizacao_categorias():
    variacoes = [
        "Violões",
        "violoes",
        "violão",
        "violao"
    ]

    resultados = [
        set(buscar_produtos(categoria, 1000)["product_id"])
        for categoria in variacoes
    ]

    assert all(
        resultado == resultados[0]
        for resultado in resultados
    )


def test_limite_preco():
    resultado = buscar_produtos("Violões", 1000)

    assert (resultado["price_brl"] <= 1000).all()


def test_disponibilidade():
    resultado = buscar_produtos("Violões", 1000)

    assert (resultado["stock_quantity"] > 0).all()
    assert (resultado["status"] == "active").all()


def test_orcamento_sem_resultados():
    resultado = buscar_produtos("Violões", 100)

    assert resultado.empty


def test_categoria_inexistente():
    resultado = buscar_produtos("Saxofones invisíveis", 1000)

    assert resultado.empty


def test_normalizacao_ukuleles():

    resultado_singular = buscar_produtos(
        "ukulele",
        preco_maximo=10000
    )

    resultado_plural = buscar_produtos(
        "ukuleles",
        preco_maximo=10000
    )

    # As duas formas devem encontrar os mesmos produtos
    assert not resultado_singular.empty

    assert resultado_singular["product_id"].tolist() == (
        resultado_plural["product_id"].tolist()
    )
