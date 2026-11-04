
# Example 03: Authorized Order Lookup

## Objective

Demonstrate how the AI agent retrieves order information
while enforcing customer-level authorization.

The application uses a simulated customer identity for
local demonstration purposes.

## Conversation

### Interaction 1: Authorized Order

**Customer:**

Quero saber o status do pedido 1

**Tool execution:**

[PEDIDO EXECUTADO] Pedido solicitado=1

**Agent:**

O pedido nº 1 já foi entregue!

Aqui estão os detalhes:

- Data do pedido: 15/10/2025
- Previsão de entrega: 25/10/2025
- Status: Entregue
- Itens: 1x Martin D-28 Dreadnought Natural
- Código de rastreio: [REDACTED]

Se precisar de mais alguma informação ou ajuda com
outro assunto, é só falar!

### Interaction 2: Unauthorized Order

**Customer:**

E o pedido 2?

**Tool execution:**

[PEDIDO EXECUTADO] Pedido solicitado=2

**Agent:**

O pedido nº 2 não foi encontrado ou não está autorizado.
Se tiver o número correto de outro pedido que deseja
verificar, é só me avisar!

## Security Design

The Gemini model can request an order using only
the order_id parameter.

The authenticated customer identifier is not supplied
by the model or extracted from the customer's message.

Instead, the Python application binds a customer identity
to the order lookup tool using a closure.

The underlying function verifies that the requested order
belongs to the customer associated with the session.

When authorization fails, the function returns a generic
error without disclosing order details.

## Technical Components

- src/pedidos.py
- src/ferramentas_pedidos.py
- src/agente.py

## Limitations

This demonstration uses DEMO_CUSTOMER_ID configured locally.

It validates authorization against a simulated session identity,
but does not implement real user authentication.

A production implementation would require a trusted
authentication mechanism and secure session management.

The tracking code was redacted from this transcript.

## Conclusion

This example demonstrates that authorization decisions
are enforced by deterministic Python code rather than
relying solely on the language model's instructions.
