from database.db import get_connection


# ---------------------------
# MATERIALS
# ---------------------------

def add_material(name, unit, min_stock):
    conn = get_connection()
    c = conn.cursor()

    name = name.strip().lower()

    c.execute(
        """
        INSERT INTO materials (name, unit, min_stock)
        VALUES (%s, %s, %s)
        ON CONFLICT (name)
        DO UPDATE SET
            unit = EXCLUDED.unit,
            min_stock = EXCLUDED.min_stock
        """,
        (name, unit, min_stock)
    )

    conn.commit()
    conn.close()


def get_materials():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, name, unit, min_stock FROM materials ORDER BY name")
    data = c.fetchall()

    conn.close()
    return data


def delete_material(material_id):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT 1 FROM bom WHERE material_id = %s LIMIT 1", (material_id,))
    if c.fetchone():
        conn.close()
        raise Exception("Material is used in BOM. Cannot delete.")

    c.execute("DELETE FROM materials WHERE id = %s", (material_id,))

    conn.commit()
    conn.close()


# ---------------------------
# TRANSACTIONS
# ---------------------------

def add_transaction(item_name, txn_type, quantity):
    conn = get_connection()
    c = conn.cursor()

    item_name = item_name.strip().lower()

    c.execute(
        """
        INSERT INTO transactions (item_name, type, quantity)
        VALUES (%s, %s, %s)
        """,
        (item_name, txn_type, quantity)
    )

    conn.commit()
    conn.close()


def get_stock():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()

    c.execute("SELECT sku FROM products")
    product_rows = c.fetchall()

    conn.close()

    product_skus = set([p[0] for p in product_rows])

    raw_materials = {}
    finished_goods = {}

    for item_name, txn_type, qty in rows:
        qty = float(qty)

        target = finished_goods if item_name in product_skus else raw_materials

        if item_name not in target:
            target[item_name] = 0

        if txn_type in ["IN", "PRODUCED"]:
            target[item_name] += qty
        elif txn_type in ["OUT", "DISPATCH"]:
            target[item_name] -= qty

    return raw_materials, finished_goods
