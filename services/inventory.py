from database.db import get_connection

def get_stock():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT item_name, quantity FROM stock")
    data = dict(c.fetchall())

    conn.close()
    return data


def update_stock(item, qty, movement):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT quantity FROM stock WHERE item_name=?", (item,))
    row = c.fetchone()
    current = row[0] if row else 0

    if movement == "OUT" and current < qty:
        conn.close()
        raise Exception(f"Not enough stock: {item}")

    new_qty = current + qty if movement == "IN" else current - qty

    c.execute("REPLACE INTO stock VALUES (?, ?)", (item, new_qty))
    conn.commit()
    conn.close()