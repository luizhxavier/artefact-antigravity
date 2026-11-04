
from src.pedidos import (
    pedidos,
    itens,
    consultar_pedido_autorizado
)


# =========================================================
# 1. CLIENTE CONSULTA O PRÓPRIO PEDIDO
# =========================================================

def test_consulta_pedido_autorizado():

    pedido = pedidos.iloc[0]

    resultado = consultar_pedido_autorizado(
        order_id=int(pedido["order_id"]),
        customer_id_autenticado=int(pedido["customer_id"])
    )

    assert "erro" not in resultado
    assert resultado["order_id"] == int(pedido["order_id"])
    assert resultado["status"] == pedido["status"]
    assert len(resultado["itens"]) == resultado["quantidade_itens"]


# =========================================================
# 2. CLIENTE TENTA CONSULTAR PEDIDO DE OUTRA PESSOA
# =========================================================

def test_consulta_pedido_outro_cliente():

    pedido = pedidos.iloc[0]

    outros_clientes = pedidos.loc[
        pedidos["customer_id"] != pedido["customer_id"],
        "customer_id"
    ]

    assert not outros_clientes.empty

    resultado = consultar_pedido_autorizado(
        order_id=int(pedido["order_id"]),
        customer_id_autenticado=int(outros_clientes.iloc[0])
    )

    assert resultado == {
        "erro": "Pedido não encontrado ou não autorizado."
    }


# =========================================================
# 3. CONSULTA DE PEDIDO INEXISTENTE
# =========================================================

def test_pedido_inexistente():

    pedido_inexistente = int(pedidos["order_id"].max()) + 1

    resultado = consultar_pedido_autorizado(
        order_id=pedido_inexistente,
        customer_id_autenticado=int(
            pedidos.iloc[0]["customer_id"]
        )
    )

    assert resultado == {
        "erro": "Pedido não encontrado ou não autorizado."
    }


# =========================================================
# 4. PEDIDO COM MÚLTIPLOS ITENS
# =========================================================

def test_pedido_com_multiplos_itens():

    contagem = itens.groupby("order_id").size()

    pedidos_multiplos = contagem.loc[contagem > 1]

    assert not pedidos_multiplos.empty

    order_id = int(pedidos_multiplos.index[0])

    cliente_id = int(
        pedidos.loc[
            pedidos["order_id"] == order_id,
            "customer_id"
        ].iloc[0]
    )

    resultado = consultar_pedido_autorizado(
        order_id=order_id,
        customer_id_autenticado=cliente_id
    )

    assert resultado["quantidade_itens"] == int(
        contagem.loc[order_id]
    )

    assert len(resultado["itens"]) > 1

    assert all(
        item["nome"] and item["quantidade"] > 0
        for item in resultado["itens"]
    )


# =========================================================
# 5. PEDIDO SEM CÓDIGO DE RASTREAMENTO
# =========================================================

def test_pedido_sem_rastreamento():

    pedido = pedidos.loc[
        pedidos["tracking_code"].isna()
    ].iloc[0]

    resultado = consultar_pedido_autorizado(
        order_id=int(pedido["order_id"]),
        customer_id_autenticado=int(pedido["customer_id"])
    )

    assert resultado["codigo_rastreio"] is None
    assert resultado["previsao_entrega"] is None


# =========================================================
# 6. PEDIDO COM CÓDIGO DE RASTREAMENTO
# =========================================================

def test_pedido_com_rastreamento():

    pedido = pedidos.loc[
        pedidos["tracking_code"].notna()
    ].iloc[0]

    resultado = consultar_pedido_autorizado(
        order_id=int(pedido["order_id"]),
        customer_id_autenticado=int(pedido["customer_id"])
    )

    assert resultado["codigo_rastreio"] == str(
        pedido["tracking_code"]
    )

    assert resultado["previsao_entrega"] == str(
        pedido["estimated_delivery"]
    )
