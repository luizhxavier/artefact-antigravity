
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from src.rag_politicas import carregar_chunks


def buscar_politicas(pergunta: str, limite: int = 2) -> list[dict]:
    """Recupera os chunks mais relevantes para uma pergunta."""

    # Carrega os 8 chunks do manual
    chunks = carregar_chunks()

    # Separa apenas o conteúdo textual
    textos = [chunk["texto"] for chunk in chunks]

    # Transforma textos em vetores TF-IDF
    vetorizador = TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        ngram_range=(1, 2)
    )

    matriz_documentos = vetorizador.fit_transform(textos)

    # Usa o mesmo vocabulário para vetorizar a pergunta
    vetor_pergunta = vetorizador.transform([pergunta])

    # Calcula a similaridade da pergunta com cada chunk
    similaridades = cosine_similarity(
        vetor_pergunta,
        matriz_documentos
    )[0]

    # Ordena os índices pela similaridade, da maior para a menor
    indices = similaridades.argsort()[::-1][:limite]

    resultados = []

    for indice in indices:
        pontuacao = float(similaridades[indice])

        if pontuacao <= 0:
            continue

        resultados.append({
            "pagina": chunks[indice]["pagina"],
            "score": round(pontuacao, 4),
            "texto": chunks[indice]["texto"]
        })

    return resultados


if __name__ == "__main__":

    perguntas = [
        "Qual o horário de funcionamento da loja?",
        "Tenho desconto pagando no PIX?",
        "Posso devolver uma compra online?"
    ]

    for pergunta in perguntas:
        print(f"\nPERGUNTA: {pergunta}")

        resultados = buscar_politicas(pergunta, limite=2)

        for resultado in resultados:
            print(
                f"\nPágina: {resultado['pagina']} | "
                f"Similaridade: {resultado['score']}"
            )

            print(resultado["texto"][:300])
