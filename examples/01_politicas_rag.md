
# Example 01: Store Policies with RAG

## Objective

Demonstrate how the AI agent retrieves information from
the store's policy manual using semantic search and
answers customer questions based on the retrieved content.

## Conversation

### Interaction 1: Business Hours

**Customer:**
Qual é o horário de funcionamento da loja?

**Tool execution:**
[RAG EXECUTADO] Pergunta: Qual é o horário de funcionamento da loja?
[RAG RECUPEROU] Páginas: [2, 1]

**Agent:**
O horário de funcionamento da Empório da Música é o seguinte:

- Segunda a Sexta-feira: das 09:00 às 18:00
- Sábado: das 09:00 às 13:00
- Domingo e Feriados: Fechado

O atendimento via WhatsApp segue o mesmo horário, com respostas
automáticas fora do expediente. Em datas especiais, o horário pode
ser estendido e avisado com antecedência.

Posso ajudar com mais alguma informação?

### Interaction 2: PIX Discount

**Customer:**
Tenho desconto pagando no PIX?

**Tool execution:**
[RAG EXECUTADO] Pergunta: Tem desconto pagando no PIX? Formas de pagamento
[RAG RECUPEROU] Páginas: [3, 6]

**Agent:**
Sim! Pagamentos realizados à vista via PIX possuem 5% de desconto
sobre o preço de tabela.

Vale ressaltar que o desconto do PIX não é cumulativo com produtos
que já estejam com preços promocionais. Se precisar de mais alguma
informação, é só falar!

## Observations

- The agent selected the policy retrieval tool for both questions.
- Semantic search retrieved the relevant manual pages.
- The answers were consistent with the store's documented policies.
- The first retrieval also included the manual cover page, which
  illustrates an opportunity to improve retrieval precision.
- This example validates observed behavior, not overall RAG accuracy.
