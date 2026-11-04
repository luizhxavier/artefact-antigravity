
from pathlib import Path

import pandas as pd

from src.catalogo import catalogo


# =========================================================
# 1. CARREGAMENTO DOS DATASETS
# =========================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

pedidos = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - orders.csv"
)

itens = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - order_items.csv"
)


# =========================================================
# 2. CONSULTA AUTORIZADA DE PEDIDOS
# =========================================================

def consultar_pedido_autorizado(
    order_id: int,
    customer_id_autenticado: int
) -> dict:
    """
    Consulta um pedido pertencente ao cliente autorizado.

    Args:
        order_id: Identificador do pedido solicitado.
        customer_id_autenticado: Identificador do cliente
            fornecido por um sistema de autenticação confiável.

    Atenção:
        Esta função verifica a posse do pedido,
        mas NÃO autentica a identidade do cliente.
    """

    # Busca somente pedidos pertencentes ao cliente autorizado
    resultado = pedidos.loc[
        (pedidos["order_id"] == order_id)
        & (pedidos["customer_id"] == customer_id_autenticado)
    ]

    # Não revela se o pedido existe ou pertence a outra pessoa
    if resultado.empty:
        return {
            "erro": "Pedido não encontrado ou não autorizado."
        }

    pedido = resultado.iloc[0]

    # Localiza os itens daquele pedido
    itens_pedido = itens.loc[
        itens["order_id"] == order_id
    ].copy()

    # Acrescenta o nome dos instrumentos
    itens_pedido = itens_pedido.merge(
        catalogo[["product_id", "name"]],
        on="product_id",
        how="left",
        validate="many_to_one"
    )

    produtos_comprados = []

    for item in itens_pedido.itertuples(index=False):

        produtos_comprados.append({
            "product_id": int(item.product_id),
            "nome": item.name,
            "quantidade": int(item.quantity)
        })

    # Trata campos que podem estar vazios
    codigo_rastreio = (
        str(pedido["tracking_code"])
        if pd.notna(pedido["tracking_code"])
        else None
    )

    previsao_entrega = (
        str(pedido["estimated_delivery"])
        if pd.notna(pedido["estimated_delivery"])
        else None
    )

    return {
        "order_id": int(pedido["order_id"]),
        "data_pedido": str(pedido["order_date"]),
        "status": str(pedido["status"]),
        "valor_total_brl": float(pedido["total_brl"]),
        "forma_pagamento": str(pedido["payment_method"]),
        "codigo_rastreio": codigo_rastreio,
        "previsao_entrega": previsao_entrega,
        "quantidade_itens": len(produtos_comprados),
        "itens": produtos_comprados
    }


# =========================================================
# 3. TESTE MANUAL COM IDENTIDADE SIMULADA
# =========================================================

if __name__ == "__main__":

    # Seleciona um pedido existente para o teste local
    exemplo = pedidos.iloc[0]

    numero_pedido = int(exemplo["order_id"])
    cliente_teste = int(exemplo["customer_id"])

    # Simula o acesso pelo dono do pedido
    autorizado = consultar_pedido_autorizado(
        order_id=numero_pedido,
        customer_id_autenticado=cliente_teste
    )

    print("\nCONSULTA AUTORIZADA")
    print("Status:", autorizado["status"])
    print("Quantidade de itens:", autorizado["quantidade_itens"])
    print(
        "Possui rastreamento:",
        autorizado["codigo_rastreio"] is not None
    )

    # Simula uma identidade que não é dona do pedido
    negado = consultar_pedido_autorizado(
        order_id=numero_pedido,
        customer_id_autenticado=-1
    )

    print("\nCONSULTA NÃO AUTORIZADA")
    print(negado)
