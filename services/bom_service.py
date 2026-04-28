from database.db import get_connection


def save_bom(product_id, material_data):
    conn = get_connection()
    c = conn.cursor()

    c.execute("DELETE FROM bom WHERE product_id = %s", (product_id,))

    for material_id, qty in material_data:
        if qty and float(qty) > 0:
            c.execute(
                """
                INSERT INTO bom (product_id, material_id, quantity)
                VALUES (%s, %s, %s)
                """,
                (product_id, material_id, qty)
            )

    conn.commit()
    conn.close()


def get_bom(product_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT m.id, m.name, b.quantity
        FROM bom b
        JOIN materials m ON b.material_id = m.id
        WHERE b.product_id = %s
        """,
        (product_id,)
    )

    data = c.fetchall()
    conn.close()
    return data
