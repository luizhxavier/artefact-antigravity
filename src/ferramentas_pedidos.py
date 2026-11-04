
from src.pedidos import consultar_pedido_autorizado


def criar_ferramenta_pedidos(customer_id_autenticado: int):
    """
    Cria uma ferramenta de consulta de pedidos vinculada
    à identidade de um cliente.

    O identificador do cliente deve vir da aplicação,
    nunca do Gemini ou de uma mensagem do usuário.
    """

    def consultar_meu_pedido(order_id: int) -> dict:
        """
        Consulta o status, os produtos e o rastreamento
        de um pedido do cliente autenticado.

        Args:
            order_id: Número do pedido que o cliente
                deseja consultar.
        """

        print(
            f"[PEDIDO EXECUTADO] Pedido solicitado={order_id}"
        )

        return consultar_pedido_autorizado(
            order_id=order_id,
            customer_id_autenticado=customer_id_autenticado
        )

    return consultar_meu_pedido
