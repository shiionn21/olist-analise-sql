import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

Path("graficos").mkdir(exist_ok=True)
conexao = sqlite3.connect("olist.db")

# 1. Top 10 categorias por faturamento
cat = pd.read_sql_query("""
    SELECT categoria, ROUND(SUM(price), 2) AS faturamento
    FROM vendas_completa
    GROUP BY categoria ORDER BY faturamento DESC LIMIT 10;
""", conexao)
plt.figure(figsize=(10, 5))
plt.barh(cat["categoria"], cat["faturamento"], color="#2e6db4")
plt.gca().invert_yaxis()
plt.title("Top 10 categorias por faturamento")
plt.xlabel("Faturamento (R$)")
plt.tight_layout()
plt.savefig("graficos/top_categorias.png", dpi=120)
plt.close()

# 2. Pedidos por estado (top 10)
est = pd.read_sql_query("""
    SELECT c.customer_state AS estado, COUNT(*) AS total
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    GROUP BY c.customer_state ORDER BY total DESC LIMIT 10;
""", conexao)
plt.figure(figsize=(10, 5))
plt.bar(est["estado"], est["total"], color="#2e6db4")
plt.title("Pedidos por estado (top 10)")
plt.ylabel("Nº de pedidos")
plt.tight_layout()
plt.savefig("graficos/pedidos_por_estado.png", dpi=120)
plt.close()

# 3. Nota média: no prazo vs atrasada
nota = pd.read_sql_query("""
    SELECT
        CASE WHEN o.order_delivered_customer_date <= o.order_estimated_delivery_date
             THEN 'No prazo' ELSE 'Atrasada' END AS entrega,
        ROUND(AVG(r.review_score), 2) AS nota_media
    FROM orders o
    JOIN order_reviews r ON o.order_id = r.order_id
    WHERE o.order_delivered_customer_date IS NOT NULL
    GROUP BY entrega ORDER BY nota_media;
""", conexao)
plt.figure(figsize=(6, 5))
plt.bar(nota["entrega"], nota["nota_media"], color=["#e5534b", "#3fb950"])
plt.title("Nota média: entrega no prazo vs atrasada")
plt.ylabel("Nota média (1-5)")
plt.ylim(0, 5)
for i, v in enumerate(nota["nota_media"]):
    plt.text(i, v + 0.1, str(v), ha="center")
plt.tight_layout()
plt.savefig("graficos/nota_vs_atraso.png", dpi=120)
plt.close()

conexao.close()
print("Gráficos salvos na pasta 'graficos/'")