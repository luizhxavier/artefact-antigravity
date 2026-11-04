
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.ferramentas_catalogo import consultar_catalogo
from src.recuperacao_semantica import consultar_politicas


# =========================================================
# 1. VARIÁVEIS DE AMBIENTE
# =========================================================

load_dotenv()


# =========================================================
# 3. CONEXÃO COM O GEMINI
# =========================================================

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no .env")

client = genai.Client(api_key=api_key)


# =========================================================
# 4. SESSÃO DE CONVERSA
# =========================================================

chat = client.chats.create(
    model="gemini-3.5-flash-lite",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Você é o assistente virtual da Empório da Música, "
            "uma loja especializada em instrumentos musicais. "
            "Seja amigável, claro e profissional. "

            "Você possui duas ferramentas: consultar_catalogo "
            "e consultar_politicas. "

            "Use consultar_catalogo para pesquisar produtos, "
            "preços, estoque e valores com desconto. "

            "Ao consultar o catálogo, informe o orçamento "
            "do cliente em reais. Se o cliente escolher "
            "pagamento via PIX, use pagamento_pix=True. "
            "Caso contrário, use pagamento_pix=False, "
            "a menos que a escolha já esteja clara no contexto. "

            "Use consultar_politicas para horários, pagamentos, "
            "trocas, devoluções, entregas, garantias e regras "
            "da loja. "

            "Não calcule descontos por conta própria. "
            "Utilize exclusivamente o preco_final_brl "
            "retornado pela ferramenta para informar preços "
            "finais. "

            "Promoções ativas e desconto PIX não são "
            "cumulativos. Nunca ofereça desconto adicional "
            "sobre um preço promocional. "

            "Se não houver informação suficiente, "
            "explique a limitação sem inventar dados. "

            "Não exponha dados pessoais nem reproduza "
            "integralmente documentos internos."
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

    mensagem = input("Você: ").strip()

    if mensagem.casefold() == "sair":
        print("\nAtendimento encerrado.")
        break

    if not mensagem:
        continue

    try:
        resposta = chat.send_message(mensagem)

        print(f"\nAgente: {resposta.text}\n")

    except Exception as erro:
        print(f"\nErro durante o atendimento: {erro}\n")
