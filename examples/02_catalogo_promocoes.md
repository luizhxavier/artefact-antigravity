
# Example 02: Product Search and Promotion Rules

## Objective

Demonstrate how the AI agent uses Function Calling to
retrieve available products and apply business rules
for promotional pricing and PIX payments.

## Customer Request

**Customer:**

Quais ukuleles vocês têm até R$ 500 pagando no PIX?

## Tool Execution

[CATÁLOGO EXECUTADO] Categoria=ukulele, Orçamento=500, PIX=True

## Agent Response

Temos ótimas opções de ukuleles até R$ 500 para pagamento
via PIX! Confira os modelos disponíveis:

- Shelby SU-21S Soprano Sunburst:
  R$ 151,91 (com 5% de desconto PIX)

- Kalani KAL-300S Soprano Natural:
  R$ 170,91 (com 5% de desconto PIX)

- Kala KA-15S Soprano Mogno:
  R$ 189,91 (com 5% de desconto PIX)

- Ohana SK-10 Soprano Natural:
  R$ 237,41 (com 5% de desconto PIX)

- Kalani KAL-700T Tenor Natural:
  R$ 323,10 (com oferta especial de 10%)

- Kala KA-C Concert Mogno:
  R$ 332,41 (com 5% de desconto PIX)

- Kala KA-T Tenor Mogno:
  R$ 427,41 (com 5% de desconto PIX)

- Ohana CK-20 Concert Natural:
  R$ 439,20 (com desconto exclusivo de 20%)

- Kalani KAL-500C Concert Elétrico Natural:
  R$ 455,05 (com 5% de desconto PIX)

Lembrando que o desconto PIX de 5% não é cumulativo
com os produtos que já estão em oferta especial.

Algum desses modelos chamou sua atenção ou gostaria
de ajuda para escolher?

## Business Rules Validated

1. Only active products with available stock are returned.
2. The budget filter uses the final discounted price.
3. Products without active promotions receive the 5%
   PIX discount when requested.
4. Products with active promotions retain their promotional
   discount without accumulating an additional PIX discount.
5. The Gemini model receives calculated prices from Python,
   rather than calculating discounts itself.

## Technical Observations

- Tool: consultar_catalogo
- Data sources: products.csv, categories.csv and promotions.csv
- Business logic: calcular_preco_final
- Pricing calculations use Python's Decimal.
- The agent returned nine eligible products.

## Conclusion

This example demonstrates the combination of LLM-based
intent interpretation with deterministic Python business
rules for product search, stock availability and pricing.
