
from pathlib import Path
import pymupdf


# Localização do manual
DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CAMINHO_PDF = DATA_DIR / "politicas_da_loja.pdf"


def carregar_chunks() -> list[dict]:
    """
    Lê o manual da loja e divide seu conteúdo
    em chunks, utilizando uma página por chunk.
    """

    chunks = []

    with pymupdf.open(CAMINHO_PDF) as documento:

        for numero, pagina in enumerate(documento, start=1):

            texto = pagina.get_text("text").strip()

            if not texto:
                continue

            chunk = {
                "id": f"politica_pagina_{numero}",
                "pagina": numero,
                "texto": texto
            }

            chunks.append(chunk)

    return chunks


if __name__ == "__main__":

    chunks = carregar_chunks()

    print(f"Total de chunks criados: {len(chunks)}")

    for chunk in chunks:
        print(
            f"{chunk['id']} | "
            f"{len(chunk['texto'])} caracteres"
        )

    # Examina o chunk correspondente à página 3
    print("\nEXEMPLO DE UM CHUNK:")

    exemplo = next(
        chunk for chunk in chunks
        if chunk["pagina"] == 3
    )

    print(exemplo["texto"][:500])
