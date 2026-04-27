from database.db import get_connection

def add_material(name, unit):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT OR IGNORE INTO materials (name, unit) VALUES (?, ?)", (name.strip().lower(), unit))
    conn.commit()
    conn.close()

def get_materials():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM materials")
    data = c.fetchall()
    conn.close()
    return data

def log_transaction(item, qty, ttype):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO transactions (item_name, quantity, type) VALUES (?, ?, ?)", (item, qty, ttype))
    conn.commit()
    conn.close()

def get_stock():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()
    conn.close()

    stock = {}
    for item, t, qty in rows:
        stock.setdefault(item, 0)
        if t == "IN":
            stock[item] += qty
        else:
            stock[item] -= qty

    return stock
