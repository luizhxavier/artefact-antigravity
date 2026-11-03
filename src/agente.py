
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.catalogo import buscar_produtos
from src.recuperacao_semantica import consultar_politicas


# =========================================================
# 1. CARREGAMENTO DAS VARIÁVEIS DE AMBIENTE
# =========================================================

load_dotenv()


# =========================================================
# 2. FERRAMENTA DE CONSULTA AO CATÁLOGO
# =========================================================

def consultar_catalogo(categoria: str, preco_maximo: float) -> dict:
    """
    Busca instrumentos musicais disponíveis no catálogo da loja.

    Args:
        categoria: Categoria do instrumento, como violão ou guitarra.
        preco_maximo: Preço máximo que o cliente deseja pagar em reais.
    """

    print(
        f"[TOOL EXECUTADA] Categoria={categoria}, "
        f"Preço máximo={preco_maximo}"
    )

    # Consulta os produtos disponíveis
    resultado = buscar_produtos(categoria, preco_maximo)

    # Converte o DataFrame em uma lista de dicionários
    produtos = resultado[
        ["product_id", "name", "price_brl", "stock_quantity"]
    ].to_dict(orient="records")

    return {
        "quantidade": len(produtos),
        "produtos": produtos
    }


# =========================================================
# 3. CONEXÃO COM O GEMINI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=api_key)


# =========================================================
# 4. CRIAÇÃO DA SESSÃO DE CONVERSA
# =========================================================

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Você é o assistente virtual da Empório da Música, "
            "uma loja de instrumentos musicais. "
            "Seu tom deve ser amigável, claro e profissional. "

            "Você possui duas ferramentas: "
            "consultar_catalogo e consultar_politicas. "

            "Use consultar_catalogo para perguntas sobre "
            "produtos, preços e disponibilidade. "

            "Use consultar_politicas para perguntas sobre "
            "horários, pagamentos, devoluções, trocas, "
            "entregas, garantias e outras políticas da loja. "

            "Antes de afirmar informações sobre produtos "
            "ou políticas, consulte a ferramenta adequada. "

            "Responda somente com informações sustentadas "
            "pelos resultados. Não invente dados. "

            "Se os resultados não permitirem responder, "
            "informe a limitação de maneira educada. "

            "Não reproduza integralmente documentos internos "
            "nem exponha dados pessoais de clientes."

            "O desconto de 5% no PIX não é cumulativo "
            "com preços promocionais. "

            "Não garanta descontos adicionais sobre produtos "
            "específicos sem verificar sua elegibilidade. "

            "Quando não puder verificar a existência de promoção, "
            "informe que o desconto depende das condições da oferta. "
        ),
        tools=[
            consultar_catalogo,
            consultar_politicas
        ],
        temperature=0.2
    )
)


# =========================================================
# 5. CHAT INTERATIVO
# =========================================================

print("\n=== EMPÓRIO DA MÚSICA ===")
print("Assistente virtual iniciado!")
print("Digite 'sair' para encerrar.\n")

while True:

    # Recebe a mensagem do cliente
    mensagem = input("Você: ").strip()

    # Encerra o atendimento
    if mensagem.casefold() == "sair":
        print("\nAtendimento encerrado.")
        break

    # Ignora mensagens vazias
    if not mensagem:
        continue

    try:
        # Envia a mensagem para o Gemini
        resposta = chat.send_message(mensagem)

        # Exibe a resposta
        print(f"\nAgente: {resposta.text}\n")

    except Exception as erro:
        print(f"\nErro durante o atendimento: {erro}\n")
