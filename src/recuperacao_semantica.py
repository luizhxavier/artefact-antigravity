
import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types
from sklearn.metrics.pairwise import cosine_similarity

from src.rag_politicas import carregar_chunks


load_dotenv()


# 1. Prepara os documentos e seus embeddings
@lru_cache(maxsize=1)
def preparar_indice():

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY não configurada")

    client = genai.Client(api_key=api_key)

    chunks = carregar_chunks()

    textos = [chunk["texto"] for chunk in chunks]

    resposta = client.models.embed_content(
        model="gemini-embedding-001",
        contents=textos,
        config=types.EmbedContentConfig(
            task_type="RETRIEVAL_DOCUMENT"
        )
    )

    vetores = [
        embedding.values
        for embedding in resposta.embeddings
    ]

    return client, chunks, vetores


# 2. Busca semântica nas políticas
def consultar_politicas(pergunta: str) -> dict:
    """
    Consulta o manual de políticas da Empório da Música.

    Args:
        pergunta: Dúvida do cliente sobre regras,
            horários, pagamentos, entregas ou devoluções.
    """
    print(
        f"[RAG EXECUTADO] Pergunta: {pergunta}",
        flush=True
    )

    client, chunks, vetores = preparar_indice()

    # Gera o embedding da pergunta
    resposta = client.models.embed_content(
        model="gemini-embedding-001",
        contents=pergunta,
        config=types.EmbedContentConfig(
            task_type="QUESTION_ANSWERING"
        )
    )

    vetor_pergunta = resposta.embeddings[0].values

    # Compara pergunta e documentos
    scores = cosine_similarity(
        [vetor_pergunta],
        vetores
    )[0]

    # Seleciona os dois chunks mais semelhantes
    indices = scores.argsort()[::-1][:2]

    trechos = []

    for indice in indices:

        trechos.append({
            "pagina": chunks[indice]["pagina"],
            "texto": chunks[indice]["texto"],
            "similaridade": round(float(scores[indice]), 4)
        })

    print(
        "[RAG RECUPEROU] Páginas:",
        [trecho["pagina"] for trecho in trechos],
        flush=True
    )

    return {"trechos": trechos}


# 3. Teste independente
if __name__ == "__main__":

    pergunta = "Qual é o horário de funcionamento da loja?"

    resultado = consultar_politicas(pergunta)

    for trecho in resultado["trechos"]:

        print(f"\nPÁGINA: {trecho['pagina']}")
        print(f"SCORE: {trecho['similaridade']}")
        print(trecho["texto"][:500])
