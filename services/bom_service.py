from database.db import get_connection

def save_bom(product_id, material_id, qty):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM bom WHERE product_id=?", (product_id,))

    c.execute("""
        INSERT INTO bom (product_id, material_id, quantity)
        VALUES (?, ?, ?)
    """, (product_id, material_id, qty))

    conn.commit()
    conn.close()

def get_bom(product_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT m.name, b.quantity
        FROM bom b
        JOIN materials m ON m.id = b.material_id
        WHERE b.product_id=?
    """, (product_id,))

    data = c.fetchall()
    conn.close()
    return data
