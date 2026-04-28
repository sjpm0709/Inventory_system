from database.db import get_connection


def produce(product_id, quantity, mode):
    if quantity <= 0:
        raise Exception("Quantity must be greater than 0")

    conn = get_connection()
    c = conn.cursor()

    # 1. BOM
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
        raise Exception("No BOM defined")

    # 2. STOCK
    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()

    stock = {}

    for item_name, txn_type, qty in rows:
        if item_name not in stock:
            stock[item_name] = 0

        if txn_type in ["IN", "PRODUCED"]:
            stock[item_name] += float(qty)
        elif txn_type in ["OUT", "DISPATCH"]:
            stock[item_name] -= float(qty)

    # 3. VALIDATION
    for material_name, per_unit_qty in bom_items:
        required = float(per_unit_qty) * float(quantity)
        available = stock.get(material_name, 0)

        if available < required:
            conn.close()
            raise Exception(f"Not enough {material_name}")

    # 4. DEDUCT MATERIALS
    for material_name, per_unit_qty in bom_items:
        required = float(per_unit_qty) * float(quantity)

        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'OUT', %s)
            """,
            (material_name, required)
        )

    # 5. FINISHED GOODS
    c.execute("SELECT sku FROM products WHERE id = %s", (product_id,))
    sku = c.fetchone()[0]

    txn_type = "PRODUCED" if mode == "stock" else "DISPATCH"

    c.execute(
        """
        INSERT INTO transactions (item_name, type, quantity)
        VALUES (%s, %s, %s)
        """,
        (sku, txn_type, quantity)
    )

    conn.commit()
    conn.close()

def dispatch_product(product_id, quantity):
    if quantity <= 0:
        raise Exception("Quantity must be greater than 0")

    conn = get_connection()
    c = conn.cursor()

    # Get SKU
    c.execute("SELECT sku FROM products WHERE id = %s", (product_id,))
    result = c.fetchone()

    if not result:
        conn.close()
        raise Exception("Product not found")

    sku = result[0]

    # Get current stock
    c.execute("SELECT item_name, type, quantity FROM transactions")
    rows = c.fetchall()

    stock = 0

    for item_name, txn_type, qty in rows:
        if item_name != sku:
            continue

        if txn_type in ["IN", "PRODUCED"]:
            stock += float(qty)
        elif txn_type in ["OUT", "DISPATCH"]:
            stock -= float(qty)

    if stock < quantity:
        conn.close()
        raise Exception(f"Not enough stock. Available: {stock}")

    # Insert dispatch transaction
    c.execute(
        """
        INSERT INTO transactions (item_name, type, quantity)
        VALUES (%s, 'DISPATCH', %s)
        """,
        (sku, quantity)
    )

    conn.commit()
    conn.close()
