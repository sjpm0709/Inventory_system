from database.db import get_connection

def add_product(sku):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO products (sku) VALUES (?)", (sku,))
    conn.commit()
    conn.close()

def get_products():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, sku FROM products")
    data = c.fetchall()
    conn.close()
    return data
