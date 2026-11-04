
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


# =========================================================
# 5. TESTES MANUAIS
# =========================================================

if __name__ == "__main__":

    print("CATEGORIAS:")
    print(categorias[["category_id", "category_name"]])

    print("\nSTATUS DOS PRODUTOS:")
    print(produtos["status"].value_counts())

    # Teste 1: diferentes formas de escrever "violão"
    categorias_teste = [
        "Violões",
        "violoes",
        "violão",
        "violao",
    ]

    print("\nTESTANDO NORMALIZAÇÃO:")

    for categoria in categorias_teste:
        resultado = buscar_produtos(categoria, 1000)

        print(
            f"Busca: {categoria} | "
            f"Produtos encontrados: {len(resultado)}"
        )

    # Teste 2: listar os violões encontrados
    print("\nVIOLÕES DISPONÍVEIS ATÉ R$ 1.000:")

    resultado = buscar_produtos("violão", 1000)

    print(
        resultado[
            ["name", "category_name", "price_brl", "stock_quantity"]
        ].to_string(index=False)
    )

    # Teste 3: orçamento muito baixo
    print("\nTESTANDO CONSULTAS SEM RESULTADOS:")

    teste_preco = buscar_produtos("Violões", 100)

    print(
        f"Violões até R$ 100: "
        f"Sem resultados? {teste_preco.empty}"
    )

    # Teste 4: categoria inexistente
    teste_categoria = buscar_produtos(
        "Saxofones invisíveis", 1000
    )

    print(
        f"Categoria inexistente: "
        f"Sem resultados? {teste_categoria.empty}"
    )


    # =====================================================
    # 6. VALIDAÇÕES AUTOMÁTICAS COM ASSERT
    # =====================================================

    print("\nVALIDANDO REGRAS DO CATÁLOGO:")

    resultado = buscar_produtos("violão", 1000)

    # Verifica se encontramos pelo menos um violão
    assert not resultado.empty, \
        "Nenhum violão encontrado"

    # Verifica se todos respeitam o limite de preço
    assert (resultado["price_brl"] <= 1000).all(), \
        "Encontrado produto acima do orçamento"

    # Verifica se todos possuem estoque disponível
    assert (resultado["stock_quantity"] > 0).all(), \
        "Encontrado produto sem estoque"

    # Verifica se todos estão ativos no catálogo
    assert (resultado["status"] == "active").all(), \
        "Encontrado produto inativo"

    # Verifica se as variações da palavra violão
    # retornam exatamente os mesmos produtos
    resultado_sem_acento = buscar_produtos("violoes", 1000)

    assert set(resultado["product_id"]) == set(
        resultado_sem_acento["product_id"]
    ), "A normalização de categorias falhou"

    # Verifica se uma busca sem produtos retorna vazio
    assert buscar_produtos("Violões", 100).empty, \
        "Encontrado produto abaixo do orçamento esperado"

    # Verifica se uma categoria inexistente retorna vazio
    assert buscar_produtos(
        "Saxofones invisíveis", 1000
    ).empty, "Categoria inexistente retornou produtos"

    print("Todas as validações passaram!")
