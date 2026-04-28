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

    # Get all transactions
    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()

    # Get all product SKUs
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

        if txn_type == "IN":
            target[item_name] += qty
        else:
            target[item_name] -= qty

    return raw_materials, finished_goods

# ---------------------------
# PRODUCTS
# ---------------------------

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

    c.execute("SELECT id, sku, name FROM products ORDER BY sku")
    data = c.fetchall()

    conn.close()
    return data


# ---------------------------
# BOM
# ---------------------------

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


# ---------------------------
# PRODUCTION (SAFE + COMPLETE)
# ---------------------------

def produce(product_id, quantity):
    conn = get_connection()
    c = conn.cursor()

    # STEP 1: Get BOM
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

    # STEP 2: Get current stock
    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()

    stock = {}

    for item_name, txn_type, qty in rows:
        if item_name not in stock:
            stock[item_name] = 0

        if txn_type == "IN":
            stock[item_name] += float(qty)
        else:
            stock[item_name] -= float(qty)

    # STEP 3: Validate stock
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

    # STEP 4: Deduct materials
    for material_name, per_unit_qty in bom_items:
        total_required = float(per_unit_qty) * float(quantity)

        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'OUT', %s)
            """,
            (material_name, total_required)
        )

    # STEP 5: Add finished goods
    c.execute("SELECT sku FROM products WHERE id = %s", (product_id,))
    sku = c.fetchone()[0]

    c.execute(
        """
        INSERT INTO transactions (item_name, type, quantity)
        VALUES (%s, 'IN', %s)
        """,
        (sku, quantity)
    )

    conn.commit()
    conn.close()

def delete_material(material_id):
    conn = get_connection()
    c = conn.cursor()

    # Check if used in BOM
    c.execute("SELECT 1 FROM bom WHERE material_id = %s LIMIT 1", (material_id,))
    if c.fetchone():
        conn.close()
        raise Exception("Material is used in BOM. Cannot delete.")

    c.execute("DELETE FROM materials WHERE id = %s", (material_id,))

    conn.commit()
    conn.close()
