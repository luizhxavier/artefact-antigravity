
from pathlib import Path
import pandas as pd
import unicodedata


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

produtos = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - products.csv"
)

categorias = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - categories.csv"
)

# Renomeia a coluna para evitar conflito com o nome dos produtos
categorias = categorias.rename(
    columns={"name": "category_name"}
)

# Relaciona os produtos às suas respectivas categorias
catalogo = produtos.merge(
    categorias[["category_id", "category_name"]],
    on="category_id",
    how="left",
    validate="many_to_one"
)


# =========================================================
# 2. NORMALIZAÇÃO DE TEXTO
# =========================================================

def normalizar_texto(texto: str) -> str:
    """Remove espaços extras, diferenças de caixa e acentos."""

    texto = texto.strip().casefold()

    texto = "".join(
        caractere
        for caractere in unicodedata.normalize("NFKD", texto)
        if not unicodedata.combining(caractere)
    )

    return texto


# =========================================================
# 3. NORMALIZAÇÃO DE CATEGORIAS
# =========================================================

def normalizar_categoria(categoria: str) -> str:
    """Converte variações de nomes para uma categoria padrão."""

    aliases = {
        "violao": "violoes",
        "violoes": "violoes",
    }

    categoria_normalizada = normalizar_texto(categoria)

    return aliases.get(
        categoria_normalizada,
        categoria_normalizada
    )


# =========================================================
# 4. FUNÇÃO DE BUSCA DE PRODUTOS
# =========================================================

def buscar_produtos(
    categoria: str,
    preco_maximo: float
) -> pd.DataFrame:
    """Busca produtos ativos, em estoque e dentro do orçamento."""

    categoria_buscada = normalizar_categoria(categoria)

    categorias_catalogo = catalogo["category_name"].map(
        normalizar_categoria
    )

    filtro = (
        (categorias_catalogo == categoria_buscada)
        & (catalogo["price_brl"] <= preco_maximo)
        & (catalogo["stock_quantity"] > 0)
        & (catalogo["status"] == "active")
    )

    resultado = catalogo.loc[filtro].copy()

    resultado = resultado.sort_values(
        by="price_brl",
        ascending=True
    )

    return resultado


