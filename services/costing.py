from database.db import get_connection

def calculate_cost(sku):
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
    SELECT b.quantity, m.cost_per_unit
    FROM bom b
    JOIN materials m ON b.material = m.name
    WHERE b.sku=?
    """, (sku,))

    total = 0
    for qty, cost in c.fetchall():
        total += qty * (cost or 0)

    conn.close()
    return total