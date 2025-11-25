"""
TASK 7 – Basic Sales Summary Using SQLite and Python
Prepared by: YOUR NAME
Date: 

Description:
This script creates a small SQLite database (sales_data.db), inserts sample
sales records, runs a simple SQL query to calculate total quantity and revenue
for each product, prints the results, and displays a basic bar chart.
"""

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# -------------------------------------------
# 1. Create database and insert sample data
# -------------------------------------------
conn = sqlite3.connect("sales_data.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS sales(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Clear table for clean execution
cur.execute("DELETE FROM sales")

# Sample entries
sample_data = [
    ("Laptop", 3, 50000),
    ("Laptop", 2, 50000),
    ("Mouse", 10, 500),
    ("Mouse", 15, 500),
    ("Keyboard", 6, 1200),
    ("Keyboard", 3, 1200)
]

cur.executemany("INSERT INTO sales(product, quantity, price) VALUES (?, ?, ?)", sample_data)
conn.commit()

# -------------------------------------------
# 2. SQL Query to compute summary
# -------------------------------------------
query = """
SELECT 
    product,
    SUM(quantity) AS total_quantity,
    SUM(quantity * price) AS total_revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)
conn.close()

# -------------------------------------------
# 3. Print Output
# -------------------------------------------
print("===== SALES SUMMARY REPORT =====")
print(df)

# -------------------------------------------
# 4. Plot Revenue Bar Chart
# -------------------------------------------
plt.figure(figsize=(7,4))
plt.bar(df["product"], df["total_revenue"])
plt.title("Revenue by Product")
plt.xlabel("Product")
plt.ylabel("Revenue (₹)")
plt.tight_layout()
plt.savefig("sales_chart.png")   # optional
plt.show()
