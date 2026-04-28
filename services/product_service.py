from database.db import get_connection


def add_product(sku, name=""):
    if not sku or not sku.strip():
        raise ValueError("SKU cannot be empty")

    sku = sku.strip().upper()
    name = name.strip() if name else ""

    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO products (sku, name)
        VALUES (%s, %s)
        ON CONFLICT (sku) DO NOTHING
        """,
        (sku, name)
    )

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        SELECT id, sku, name
        FROM products
        ORDER BY sku
        """
    )

    data = c.fetchall()
    conn.close()
    return data
