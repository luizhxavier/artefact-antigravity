
from src.catalogo import buscar_produtos
from src.promocoes import calcular_preco_final


def consultar_catalogo(
    categoria: str,
    preco_maximo: float,
    pagamento_pix: bool = False
) -> dict:
    """
    Consulta instrumentos disponíveis e calcula preços finais.

    Args:
        categoria: Categoria do instrumento, como violão ou ukulele.
        preco_maximo: Orçamento máximo do cliente em reais.
        pagamento_pix: True se o cliente escolher pagar via PIX.
    """

    print(
        f"[CATÁLOGO EXECUTADO] Categoria={categoria}, "
        f"Orçamento={preco_maximo}, PIX={pagamento_pix}"
    )

    if preco_maximo < 0:
        return {"erro": "O orçamento não pode ser negativo."}

    candidatos = buscar_produtos(
        categoria=categoria,
        preco_maximo=float("inf")
    )

    produtos = []

    for produto in candidatos.itertuples(index=False):

        precificacao = calcular_preco_final(
            product_id=int(produto.product_id),
            pagamento_pix=pagamento_pix
        )

        if "erro" in precificacao:
            continue

        preco_final = precificacao["preco_final_brl"]

        if preco_final > preco_maximo:
            continue

        produtos.append({
            "product_id": int(produto.product_id),
            "nome": precificacao["nome"],
            "preco_tabela_brl": precificacao["preco_tabela_brl"],
            "preco_final_brl": preco_final,
            "tipo_desconto": precificacao["tipo_desconto"],
            "percentual_desconto": precificacao["percentual_desconto"],
            "descricao_desconto": precificacao["descricao"],
            "estoque": int(produto.stock_quantity)
        })

    produtos.sort(
        key=lambda item: item["preco_final_brl"]
    )

    return {
        "categoria": categoria,
        "orcamento_brl": preco_maximo,
        "pagamento_pix": pagamento_pix,
        "regra": (
            "O desconto PIX de 5% não é cumulativo "
            "com promoções ativas."
        ),
        "quantidade": len(produtos),
        "produtos": produtos
    }
