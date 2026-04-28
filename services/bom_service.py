from database.db import get_connection


def save_bom(product_id, material_data):
    """
    material_data = [(material_id, qty), ...]
    """

    conn = get_connection()
    c = conn.cursor()

    # Delete old BOM
    c.execute("DELETE FROM bom WHERE product_id = %s", (product_id,))

    # Insert new BOM (multiple materials)
    for material_id, qty in material_data:
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
        SELECT m.name, b.quantity
        FROM bom b
        JOIN materials m ON m.id = b.material_id
        WHERE b.product_id = %s
        """,
        (product_id,)
    )

    data = c.fetchall()
    conn.close()
    return data
