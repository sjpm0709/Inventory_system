from database.db import get_connection


# ---------------------------
# MATERIALS
# ---------------------------

def add_material(name, unit):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO materials (name, unit)
        VALUES (%s, %s)
        ON CONFLICT (name) DO NOTHING
        """,
        (name.strip().lower(), unit)
    )

    conn.commit()
    conn.close()


def get_materials():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, name, unit FROM materials ORDER BY name")
    data = c.fetchall()

    conn.close()
    return data


# ---------------------------
# STOCK TRANSACTIONS
# ---------------------------

def add_transaction(item_name, txn_type, quantity):
    conn = get_connection()
    c = conn.cursor()

    # normalize
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

    conn.close()

    stock = {}

    for item_name, txn_type, qty in rows:
        if item_name not in stock:
            stock[item_name] = 0

        if txn_type == "IN":
            stock[item_name] += float(qty)
        else:
            stock[item_name] -= float(qty)

    return stock


# ---------------------------
# PRODUCTS (SKU)
# ---------------------------

def add_product(sku, name):
    conn = get_connection()
    c = conn.cursor()

    c.execute(
        """
        INSERT INTO products (sku, name)
        VALUES (%s, %s)
        ON CONFLICT (sku) DO NOTHING
        """,
        (sku.strip().upper(), name.strip())
    )

    conn.commit()
    conn.close()


def get_products():
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT id, sku, name FROM products ORDER BY sku")
    data = c.fetchall()

    conn.close()
    return data


# ---------------------------
# BOM (Bill of Materials)
# ---------------------------

def save_bom(product_id, material_data):
    """
    material_data = list of tuples:
    [(material_id, qty), ...]
    """

    conn = get_connection()
    c = conn.cursor()

    # remove old BOM
    c.execute("DELETE FROM bom WHERE product_id = %s", (product_id,))

    # insert new
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


# ---------------------------
# PRODUCTION
# ---------------------------

def produce(product_id, quantity):
    conn = get_connection()
    c = conn.cursor()

    # ---------------------------
    # STEP 1: Get BOM
    # ---------------------------
    c.execute(
        """
        SELECT m.name, b.quantity
        FROM bom b
        JOIN materials m ON b.material_id = m.id
        WHERE b.product_id = %s
        """,
        (product_id,)
    )

    bom_items = c.fetchall()

    if not bom_items:
        conn.close()
        raise Exception("No BOM defined for this product")

    # ---------------------------
    # STEP 2: Get current stock
    # ---------------------------
    c.execute(
        """
        SELECT item_name, type, quantity
        FROM transactions
        """
    )

    rows = c.fetchall()

    stock = {}

    for item_name, txn_type, qty in rows:
        if item_name not in stock:
            stock[item_name] = 0

        if txn_type == "IN":
            stock[item_name] += float(qty)
        else:
            stock[item_name] -= float(qty)

    # ---------------------------
    # STEP 3: Validate stock
    # ---------------------------
    shortages = []

    for material_name, per_unit_qty in bom_items:
        required = float(per_unit_qty) * float(quantity)
        available = stock.get(material_name, 0)

        if available < required:
            shortages.append(
                f"{material_name} (Required: {required}, Available: {available})"
            )

    if shortages:
        conn.close()
        raise Exception("Insufficient stock:\n" + "\n".join(shortages))

    # ---------------------------
    # STEP 4: Deduct materials
    # ---------------------------
    for material_name, per_unit_qty in bom_items:
        total_required = float(per_unit_qty) * float(quantity)

        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'OUT', %s)
            """,
            (material_name, total_required)
        )

    conn.commit()
    conn.close()
