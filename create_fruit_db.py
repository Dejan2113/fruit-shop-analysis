"""
Fruit Shop – practice database (fictional data)

Creates fruit_shop.db with 3 tables:
  products  – 7 fruits with price per kg
  stores    – 2 shops (Bitola, Ohrid)
  sales     – daily sales per fruit per shop, July–September 2026
  

Run:  python create_fruit_db.py
"""
import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

random.seed(42)  # same numbers every time you run it

DB_PATH = Path(__file__).parent / "fruit_shop.db"
if DB_PATH.exists():
    DB_PATH.unlink()

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

# ---------- tables ----------
cur.executescript("""
CREATE TABLE products (
    product_id   INTEGER PRIMARY KEY,
    name         TEXT NOT NULL,
    price_per_kg REAL NOT NULL      -- in denars (MKD)
);

CREATE TABLE stores (
    store_id INTEGER PRIMARY KEY,
    city     TEXT NOT NULL
);

CREATE TABLE sales (
    sale_id     INTEGER PRIMARY KEY,
    sale_date   TEXT NOT NULL,      -- 'YYYY-MM-DD'
    product_id  INTEGER NOT NULL REFERENCES products(product_id),
    store_id    INTEGER NOT NULL REFERENCES stores(store_id),
    quantity_kg REAL NOT NULL,
    revenue     REAL NOT NULL       -- quantity_kg * price_per_kg
);
""")

# ---------- products ----------
products = [
    (1, "Apple",      60),
    (2, "Banana",     90),
    (3, "Orange",     80),
    (4, "Watermelon", 25),
    (5, "Grapes",    110),
    (6, "Strawberry", 220),
    (7, "Peach",      95),
]
cur.executemany("INSERT INTO products VALUES (?, ?, ?)", products)

stores = [(1, "Bitola"), (2, "Ohrid")]
cur.executemany("INSERT INTO stores VALUES (?, ?)", stores)

# ---------- sales ----------
# average kg per day, per month (7 = July, 8 = August, 9 = September)
# seasonal: watermelon & peach peak in summer, apple & grapes grow in September
base_kg = {
    "Apple":      {7: 18, 8: 20, 9: 32},
    "Banana":     {7: 25, 8: 24, 9: 26},
    "Orange":     {7: 10, 8: 9,  9: 14},
    "Watermelon": {7: 70, 8: 80, 9: 30},
    "Grapes":     {7: 5,  8: 15, 9: 28},
    "Strawberry": {7: 8,  8: 4,  9: 2},
    "Peach":      {7: 22, 8: 26, 9: 10},
}
# Ohrid has tourists in summer -> sells more in July/August
store_factor = {"Bitola": {7: 1.0, 8: 1.0, 9: 1.0},
                "Ohrid":  {7: 1.4, 8: 1.5, 9: 0.9}}

start, end = date(2026, 7, 1), date(2026, 9, 30)
rows = []
d = start
while d <= end:
    weekend = 1.25 if d.weekday() >= 5 else 1.0
    for pid, name, price in products:
        for sid, city in stores:
            mean = base_kg[name][d.month] * store_factor[city][d.month] * weekend
            kg = max(0.5, round(random.gauss(mean, mean * 0.2), 1))
            rows.append((d.isoformat(), pid, sid, kg, round(kg * price, 0)))
    d += timedelta(days=1)

cur.executemany(
    "INSERT INTO sales (sale_date, product_id, store_id, quantity_kg, revenue) "
    "VALUES (?, ?, ?, ?, ?)",
    rows,
)

conn.commit()
print(f"Created {DB_PATH.name}: {len(products)} products, {len(stores)} stores, {len(rows)} sales rows")
conn.close()
