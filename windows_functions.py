import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path(__file__).parent/"fruit_shop.db")

for red in conn.execute("""
WITH totals AS (
        SELECT stores.city, products.name, SUM(sales.revenue) AS total_revenue
        FROM sales
        JOIN stores ON stores.store_id = sales.store_id
        JOIN products ON products.product_id = sales.product_id
        GROUP BY city, name
        ),
ranked AS(
    SELECT city, name, total_revenue,
            ROW_NUMBER() OVER (PARTITION BY city ORDER BY total_revenue DESC) AS rn
        FROM totals
    )
    SELECT * FROM ranked
    WHERE rn <= 2
"""):
    print(red)

print("----Ecercise")

for row in conn.execute("""
WITH totals AS(
            SELECT strftime('%m', sales.sale_date) AS month, products.name, SUM(sales.revenue) AS total_revenue
            FROM sales
            JOIN products ON products.product_id = sales.product_id
            GROUP BY month, products.name
            ),
    ranked AS(
        SELECT month, name, total_revenue,
            ROW_NUMBER() OVER(PARTITION BY month ORDER BY total_revenue ASC) AS rn
        FROM totals
)
SELECT * FROM ranked
WHERE rn = 1
"""):
    print(row)

# products: product_id, name, price_per_kg
# stores:   store_id, city
# sales:    sale_id, sale_date, product_id, store_id, quantity_kg, revenu

conn.close()