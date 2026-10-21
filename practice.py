import sqlite3
from pathlib import Path

conn = sqlite3.connect(Path(__file__).parent/"fruit_shop.db")


print("-----Excercise 1")
for red in conn.execute("""
                        SELECT products.name, SUM(sales.quantity_kg) AS total_kg
                        FROM sales
                        JOIN products ON sales.product_id = products.product_id
                        GROUP BY products.name

"""):
    print(red)

print("----Excercise 2")
for red in conn.execute("""
                        SELECT products.name, SUM(sales.revenue) AS total_revenue
                        FROM sales
                        JOIN products ON sales.product_id = products.product_id
                        GROUP BY products.name
                        ORDER BY total_revenue DESC
"""):
    print(red)

print("----Excercise 3")
for red in conn.execute("""
                        SELECT stores.city, SUM(sales.revenue) AS total_revenue
                        FROM sales
                        JOIN stores ON stores.store_id = sales.store_id
                        GROUP BY stores.city
                        ORDER BY total_revenue ASC
"""):
    print(red)

print("----Excercise 4")
for red in conn.execute("""
                        SELECT stores.city, strftime('%m', sales.sale_date) AS month, SUM(sales.revenue) AS total_revenue
                        FROM sales 
                        JOIN stores ON stores.store_id = sales.store_id
                        GROUP BY stores.city, month
                        ORDER BY city, month
"""):
    print(red)

print("----Excercise 5")


#Exercise 5: Финалето 🏆 (сè што научи денес заедно)

# Кое овошје донело најмногу пари во секој месец?

# Резултатот треба да е 3 реда, по еден за секој месец:

# month	name	total_revenue
# 07	???	...
# 08	???	...
# 09	???	...

# Ова е класично интервју прашање, исто како „најскапиот стан по град“ од утрово, само со овошје. 😉

# Чекор по чекор:

# Прво, без window function: направи query што покажува month, name и SUM(revenue) за секое овошје во секој месец (21 ред). Тоа е спој од Exercise 2 и Exercise 4.
# Потоа, стави го тоа query во CTE (WITH ... AS (...)) и додади ROW_NUMBER() OVER (PARTITION BY ___ ORDER BY ___ DESC).
# Надвор од CTE, филтрирај WHERE rn = 1.

query = """
WITH monthly AS(
    SELECT strftime('%m', sales.sale_date) AS month, products.name, SUM(sales.revenue) AS total_revenue
    FROM sales
    JOIN products ON sales.product_id = products.product_id
    GROUP BY month, products.name
    ),
ranked as(
SELECT month, name, total_revenue,
    ROW_NUMBER() OVER (PARTITION BY month ORDER BY total_revenue) AS rn
    FROM monthly
)
SELECT * FROM ranked
WHERE rn = 1
ORDER BY total_revenue DESC
"""
for row in conn.execute(query):
    print(row)

print("----Excercise 6")
for red in conn.execute("""
                        SELECT stores.city,  SUM(sales.quantity_kg) AS total_kg 
                        FROM SALES
                        JOIN stores ON stores.store_id = sales.store_id
                        GROUP BY stores.city

"""):   
    print(red)

    

print("----Excercise 7")
for red in conn.execute("""
                        SELECT stores.city, SUM(sales.revenue) as total_revenue
                        FROM sales
                        JOIN stores ON stores.store_id = sales.store_id
                        GROUP BY city
                        ORDER BY total_revenue DESC

"""):
    print(red)


print("----Ecercise 8")
for red in conn.execute("""
                        SELECT stores.store_id, SUM(sales.quantity_kg) AS total_kg
                        FROM sales
                        JOIN stores ON stores.store_id = sales.store_id
                        GROUP BY stores.store_id
                        ORDER BY total_kg DESC
                        
"""):
    print(red)



print("----Excercise 9")
for red in conn.execute("""
                        SELECT stores.store_id, SUM(sales.quantity_kg) AS total_kg
                        FROM sales
                        JOIN stores ON stores.store_id = sales.store_id
                        JOIN products on products.product_id = sales.product_id
                        WHERE products.name = "WATERMELON"
                        GROUP BY stores.store_id
                        ORDER BY total_kg DESC
"""): 
    print(red)


print("----Ecercise 10")
for red in conn.execute("""
                        SELECT products.name, SUM(sales.quantity_kg) AS total_kg
                        FROM sales
                        JOIN products ON products.product_id = sales.product_id
                        GROUP BY products.name
                        HAVING total_kg > 5000

"""):
    print(red)



print("----Ecercise 11")
for red in conn.execute("""
                        SELECT products.name, ROUND(AVG(sales.quantity_kg), 1) as avg_kg
                        FROM sales
                        JOIN stores ON stores.store_id = sales.store_id
                        JOIN products ON products.product_id = sales.product_id
                        WHERE stores.city = 'Ohrid'
                        GROUP BY products.name
                        ORDER BY avg_kg DESC
"""):
    print(red)



print("----Excercise 12")
for red in conn.execute("""
                        SELECT sales.sale_date, SUM(sales.revenue) AS total_revenue
                        FROM sales
                        WHERE strftime('%m', sales.sale_date) = '08'
                        GROUP BY sales.sale_date
                        ORDER BY total_revenue DESC
                        LIMIT 1

"""):
    print(red)

# products: product_id, name, price_per_kg
# stores:   store_id, city
# sales:    sale_id, sale_date, product_id, store_id, quantity_kg, revenu

print("----Excercise 13")
for red in conn.execute("""
                        SELECT products.name, SUM(sales.revenue) as total_revenue
                        FROM sales
                        JOIN products ON products.product_id = sales.product_id
                        WHERE strftime('%m', sales.sale_date) = '07'
                        GROUP BY products.name
                        ORDER BY total_revenue DESC
                        LIMIT 3
"""):
    print(red)


conn.close()
