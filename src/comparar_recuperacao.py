
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity

from src.rag_politicas import carregar_chunks
from src.buscar_politicas import buscar_politicas


# 1. Configuração da API
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY não configurada")

client = genai.Client(api_key=api_key)


# 2. Carregamento dos documentos
chunks = carregar_chunks()

textos = [chunk["texto"] for chunk in chunks]


# 3. Geração dos embeddings dos documentos
resposta_documentos = client.models.embed_content(
    model="gemini-embedding-001",
    contents=textos,
    config=types.EmbedContentConfig(
        task_type="RETRIEVAL_DOCUMENT"
    )
)

vetores_documentos = [
    embedding.values
    for embedding in resposta_documentos.embeddings
]


# 4. Perguntas para comparar as duas abordagens
perguntas = [
    "Em quais dias e horários posso visitar a loja?",
    "Se pagar por transferência instantânea, ganho vantagem?",
    "Comprei online e mudei de ideia. Posso desfazer a compra?"
]


# 5. Comparação entre TF-IDF e embeddings
for pergunta in perguntas:

    # Recuperação tradicional
    resultado_tfidf = buscar_politicas(
        pergunta,
        limite=1
    )

    # Embedding da pergunta
    resposta_pergunta = client.models.embed_content(
        model="gemini-embedding-001",
        contents=pergunta,
        config=types.EmbedContentConfig(
            task_type="QUESTION_ANSWERING"
        )
    )

    vetor_pergunta = resposta_pergunta.embeddings[0].values

    # Similaridade semântica
    scores = cosine_similarity(
        [vetor_pergunta],
        vetores_documentos
    )[0]

    melhor_indice = scores.argmax()

    print(f"\nPERGUNTA: {pergunta}")

    if resultado_tfidf:
        print(
            "TF-IDF -> Página:",
            resultado_tfidf[0]["pagina"]
        )
    else:
        print("TF-IDF -> Nenhuma página recuperada")

    print(
        "EMBEDDINGS -> Página:",
        chunks[melhor_indice]["pagina"]
    )

    print(
        "Score semântico:",
        round(float(scores[melhor_indice]), 4)
    )
