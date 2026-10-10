import sqlite3

conexao = sqlite3.connect("olist.db")
cursor = conexao.cursor()

# VIEW: uma "tabela virtual" que já deixa as vendas prontas (juntadas)
cursor.execute("DROP VIEW IF EXISTS vendas_completa;")
cursor.execute("""
    CREATE VIEW vendas_completa AS
    SELECT
        oi.order_id,
        ct.product_category_name_english AS categoria,
        oi.price,
        oi.freight_value,
        o.order_purchase_timestamp,
        c.customer_state
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    JOIN category_translation ct ON p.product_category_name = ct.product_category_name
    JOIN orders o ON oi.order_id = o.order_id
    JOIN customers c ON o.customer_id = c.customer_id;
""")

# ÍNDICES: aceleram os JOINs e filtros nas colunas mais usadas
cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_items_order ON order_items(order_id);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);")

conexao.commit()
conexao.close()
print("View e índices criados!")