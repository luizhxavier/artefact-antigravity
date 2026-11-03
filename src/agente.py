
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.catalogo import buscar_produtos


# 1. Carrega nossa chave de API
load_dotenv()


# 2. Ferramenta que o Gemini poderá solicitar
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

    # Reutiliza a função que já construímos
    resultado = buscar_produtos(categoria, preco_maximo)

    # Transforma o DataFrame em uma lista de dicionários
    produtos = resultado[
        ["product_id", "name", "price_brl", "stock_quantity"]
    ].to_dict(orient="records")

    return {
        "quantidade": len(produtos),
        "produtos": produtos
    }


# 3. Conexão com o Gemini
client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


# =========================================================
# 4. CRIAÇÃO DA SESSÃO DE CONVERSA
# =========================================================

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Você é um atendente da Empório da Música, "
            "uma loja especializada em instrumentos musicais. "
            "Seja cordial, claro e objetivo. "
            "Sempre consulte a ferramenta disponível antes "
            "de informar preços ou estoque. "
            "Nunca invente produtos, preços ou disponibilidade. "
            "Se não tiver dados suficientes para responder, "
            "informe isso ao cliente."
        ),
        tools=[consultar_catalogo],
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

    mensagem = input("Você: ").strip()

    # Encerra a conversa
    if mensagem.casefold() == "sair":
        print("\nAtendimento encerrado.")
        break

    # Ignora mensagens vazias
    if not mensagem:
        continue

    try:
        # Envia a mensagem para o Gemini
        resposta = chat.send_message(mensagem)

        # Exibe a resposta do agente
        print(f"\nAgente: {resposta.text}\n")

    except Exception as erro:
        print(f"\nErro durante o atendimento: {erro}\n")

# Cria uma sessão de conversa com o Gemini
chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Você é um atendente da Empório da Música. "
            "Para informar preços e estoque, consulte a ferramenta "
            "disponível. Nunca invente produtos ou valores."
        ),
        tools=[consultar_catalogo],
        temperature=0.2
    )
)

# Envia a mensagem dentro da sessão
resposta = chat.send_message(pergunta)



# 6. Mostra a resposta final
print("\nRESPOSTA DO AGENTE:")
print(resposta.text)
