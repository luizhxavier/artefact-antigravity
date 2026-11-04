
import inspect

from src.pedidos import pedidos
from src.ferramentas_pedidos import criar_ferramenta_pedidos


def test_ferramenta_consulta_pedido_do_cliente():

    pedido = pedidos.iloc[0]

    ferramenta = criar_ferramenta_pedidos(
        customer_id_autenticado=int(pedido["customer_id"])
    )

    resultado = ferramenta(
        order_id=int(pedido["order_id"])
    )

    assert "erro" not in resultado
    assert resultado["order_id"] == int(pedido["order_id"])


def test_ferramenta_bloqueia_outro_cliente():

    pedido = pedidos.iloc[0]

    outro_cliente = pedidos.loc[
        pedidos["customer_id"] != pedido["customer_id"]
    ].iloc[0]

    ferramenta = criar_ferramenta_pedidos(
        customer_id_autenticado=int(
            outro_cliente["customer_id"]
        )
    )

    resultado = ferramenta(
        order_id=int(pedido["order_id"])
    )

    assert resultado == {
        "erro": "Pedido não encontrado ou não autorizado."
    }


def test_gemini_nao_recebe_parametro_customer_id():

    pedido = pedidos.iloc[0]

    ferramenta = criar_ferramenta_pedidos(
        customer_id_autenticado=int(pedido["customer_id"])
    )

    assinatura = inspect.signature(ferramenta)

    assert list(assinatura.parameters) == ["order_id"]
