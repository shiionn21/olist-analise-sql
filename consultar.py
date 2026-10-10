import sqlite3
import pandas as pd

conexao = sqlite3.connect("olist.db")

consultas = {
    "Faturamento por categoria (usando a VIEW)": """
        SELECT categoria, ROUND(SUM(price), 2) AS faturamento
        FROM vendas_completa
        GROUP BY categoria
        ORDER BY faturamento DESC
        LIMIT 5;
    """,
}

for titulo, query in consultas.items():
    print(f"\n=== {titulo} ===")
    print(pd.read_sql_query(query, conexao))

conexao.close()