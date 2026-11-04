
from pathlib import Path

import pandas as pd


# =========================================================
# 1. CARREGAMENTO DOS DADOS
# =========================================================

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

clientes = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - customers.csv"
)

pedidos = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - orders.csv"
)

itens = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - order_items.csv"
)

produtos = pd.read_csv(
    DATA_DIR / "desafio_tecnico_ai_eng - products.csv"
)


# =========================================================
# 2. VERIFICAÇÃO DE CHAVES PRIMÁRIAS
# =========================================================

print("\nCHAVES PRIMÁRIAS DUPLICADAS:")

print(
    "Clientes:",
    clientes["customer_id"].duplicated().sum()
)

print(
    "Pedidos:",
    pedidos["order_id"].duplicated().sum()
)

print(
    "Produtos:",
    produtos["product_id"].duplicated().sum()
)


# =========================================================
# 3. VERIFICAÇÃO DOS RELACIONAMENTOS
# =========================================================

# Pedidos cujo cliente não existe
pedidos_sem_cliente = pedidos.loc[
    ~pedidos["customer_id"].isin(clientes["customer_id"])
]

# Itens cujo pedido não existe
itens_sem_pedido = itens.loc[
    ~itens["order_id"].isin(pedidos["order_id"])
]

# Itens cujo produto não existe
itens_sem_produto = itens.loc[
    ~itens["product_id"].isin(produtos["product_id"])
]

# Pedidos sem nenhum item cadastrado
pedidos_sem_itens = pedidos.loc[
    ~pedidos["order_id"].isin(itens["order_id"])
]


print("\nINTEGRIDADE REFERENCIAL:")

print(
    "Pedidos com cliente inexistente:",
    len(pedidos_sem_cliente)
)

print(
    "Itens com pedido inexistente:",
    len(itens_sem_pedido)
)

print(
    "Itens com produto inexistente:",
    len(itens_sem_produto)
)

print(
    "Pedidos sem itens:",
    len(pedidos_sem_itens)
)


# =========================================================
# 4. DISTRIBUIÇÃO DE ITENS POR PEDIDO
# =========================================================

quantidade_itens = itens.groupby("order_id").size()

print("\nITENS POR PEDIDO:")

print(quantidade_itens.value_counts().sort_index())


# =========================================================
# 5. RASTREAMENTO POR STATUS
# =========================================================

print("\nRASTREAMENTO POR STATUS:")

resumo = pedidos.groupby("status").agg(
    total_pedidos=("order_id", "count"),
    com_rastreamento=("tracking_code", "count"),
    com_previsao=("estimated_delivery", "count")
)

print(resumo)
