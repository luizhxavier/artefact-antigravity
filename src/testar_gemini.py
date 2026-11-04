
import os
from dotenv import load_dotenv
from google import genai

# Carrega as variáveis do arquivo .env
load_dotenv()

# Recupera a chave de API
api_key = os.getenv("GEMINI_API_KEY")

# Verifica se a chave foi configurada
if not api_key:
    raise ValueError("GEMINI_API_KEY não encontrada!")

# Cria o cliente da API
client = genai.Client(api_key=api_key)

# Envia uma mensagem ao modelo
resposta = client.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents="Responda apenas: Conexão estabelecida."
)

# Exibe a resposta do modelo
print(resposta.text)
