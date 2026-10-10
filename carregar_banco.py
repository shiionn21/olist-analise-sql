import sqlite3
import pandas as pd
from pathlib import Path

# Cria (ou abre) o arquivo do banco
conexao = sqlite3.connect("olist.db")

# De cada arquivo CSV -> um nome de tabela limpo e curto
mapa = {
    "olist_customers_dataset.csv": "customers",
    "olist_orders_dataset.csv": "orders",
    "olist_order_items_dataset.csv": "order_items",
    "olist_order_payments_dataset.csv": "order_payments",
    "olist_order_reviews_dataset.csv": "order_reviews",
    "olist_products_dataset.csv": "products",
    "olist_sellers_dataset.csv": "sellers",
    "olist_geolocation_dataset.csv": "geolocation",
    "product_category_name_translation.csv": "category_translation",
}

for arquivo, tabela in mapa.items():
    df = pd.read_csv(Path("dados") / arquivo)
    df.to_sql(tabela, conexao, if_exists="replace", index=False)
    print(f"Tabela '{tabela}' criada com {len(df)} linhas.")

# Primeiro teste de SQL: contar os pedidos
teste = pd.read_sql_query("SELECT COUNT(*) AS total_pedidos FROM orders", conexao)
print("\nTeste — total de pedidos:", teste["total_pedidos"][0])

conexao.close()
print("Banco 'olist.db' pronto!")