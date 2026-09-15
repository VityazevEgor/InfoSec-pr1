import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'app.db')

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL NOT NULL
        )
    """)
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO products (name, price) VALUES (?, ?)", [
            ("Ноутбук", 75000.0),
            ("Смартфон", 45000.0),
            ("Клавиатура", 3500.0)
        ])
    conn.commit()
    conn.close()

def search_products(query):
    conn = get_connection()
    cursor = conn.cursor()
    # Безопасный параметризованный SQL-запрос
    sql = "SELECT * FROM products WHERE name LIKE ?"
    cursor.execute(sql, (f"%{query}%",))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
