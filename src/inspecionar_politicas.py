
from pathlib import Path
import pymupdf

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CAMINHO_PDF = DATA_DIR / "politicas_da_loja.pdf"

# Abre o documento
with pymupdf.open(CAMINHO_PDF) as documento:
    print(f"Total de páginas: {len(documento)}")

    # Percorre cada página do PDF
    for numero, pagina in enumerate(documento, start=1):
        texto = pagina.get_text()

        print(
            f"Página {numero}: "
            f"{len(texto)} caracteres extraídos"
        )

        # Mostra uma pequena amostra do conteúdo
        if numero == 2:
            print("\nAMOSTRA DA PÁGINA 2:")
            print(texto[:1200])
