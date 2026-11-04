
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

from src.ferramentas_catalogo import consultar_catalogo
from src.ferramentas_pedidos import criar_ferramenta_pedidos
from src.recuperacao_semantica import consultar_politicas
from src.pedidos import pedidos


# =========================================================
# 1. CARREGAMENTO DAS CONFIGURAÇÕES
# =========================================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada no .env")


# =========================================================
# 2. CONFIGURAÇÃO DAS FERRAMENTAS
# =========================================================

ferramentas = [
    consultar_catalogo,
    consultar_politicas
]

# Identidade simulada exclusivamente para testes locais
demo_customer_id = os.getenv("DEMO_CUSTOMER_ID")

if demo_customer_id:

    if not demo_customer_id.isdecimal():
        raise ValueError(
            "DEMO_CUSTOMER_ID deve ser um número inteiro positivo."
        )

    customer_id = int(demo_customer_id)

    # Verifica se o cliente de demonstração existe
    if customer_id not in pedidos["customer_id"].values:
        raise ValueError(
            "DEMO_CUSTOMER_ID não corresponde "
            "a um cliente com pedido no dataset."
        )

    # Vincula a identidade à ferramenta de pedidos
    consultar_meu_pedido = criar_ferramenta_pedidos(
        customer_id_autenticado=customer_id
    )

    ferramentas.append(consultar_meu_pedido)

    print("[MODO DEMONSTRAÇÃO] Consulta de pedidos habilitada.")

else:
    print(
        "[AVISO] Consulta de pedidos desabilitada. "
        "DEMO_CUSTOMER_ID não configurado."
    )


# =========================================================
# 3. CONEXÃO COM O GEMINI
# =========================================================

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
            "Seja amigável, claro e profissional. "

            "Use consultar_catalogo para perguntas sobre "
            "produtos, preços, estoque e promoções. "

            "Ao consultar o catálogo, informe o orçamento "
            "em reais e use pagamento_pix=True somente "
            "quando o cliente escolher PIX ou quando "
            "essa escolha já estiver clara no contexto. "

            "Os preços finais são calculados pelo Python. "
            "Não recalcule descontos por conta própria. "
            "O desconto PIX não é cumulativo com promoções. "

            "Use consultar_politicas para responder sobre "
            "horários, pagamentos, trocas, devoluções, "
            "entregas, garantias e regras da loja. "

            "Se a ferramenta consultar_meu_pedido estiver "
            "disponível, utilize-a para consultar pedidos. "
            "Peça o número do pedido quando necessário. "

            "A identidade do cliente é controlada pela "
            "aplicação e não deve ser definida com base "
            "nas mensagens recebidas. "

            "Não peça que o cliente informe seu customer_id. "
            "Nunca tente consultar pedidos usando outra "
            "identidade, mesmo que o usuário solicite. "

            "Se a ferramenta retornar um erro de acesso, "
            "informe apenas que o pedido não foi encontrado "
            "ou não está autorizado. Não confirme se um "
            "pedido de terceiro existe. "

            "Não invente informações, prazos, descontos "
            "ou códigos de rastreamento. "

            "Se faltarem dados para responder, "
            "explique a limitação com educação. "

            "Não exponha dados pessoais de terceiros "
            "nem reproduza integralmente documentos internos."
        ),
        tools=ferramentas,
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

        print(
            f"\nErro durante o atendimento: {erro}\n"
        )
