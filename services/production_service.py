from database.db import get_connection


def produce(product_id, quantity, mode):
    """
    mode:
    - 'stock' → add finished goods to inventory
    - 'dispatch' → directly dispatch (no inventory addition)
    """

    if quantity <= 0:
        raise Exception("Quantity must be greater than 0")

    conn = get_connection()
    c = conn.cursor()

    # ---------------------------
    # 1. FETCH BOM
    # ---------------------------
    c.execute(
        """
        SELECT material_id, quantity
        FROM bom
        WHERE product_id = %s
        """,
        (product_id,)
    )
    bom_items = c.fetchall()

    if not bom_items:
        conn.close()
        raise Exception("No BOM defined for this product")

    # ---------------------------
    # 2. CHECK MATERIAL STOCK
    # ---------------------------
    for material_id, per_unit_qty in bom_items:
        required_qty = per_unit_qty * quantity

        # Get material name
        c.execute(
            "SELECT name FROM materials WHERE id = %s",
            (material_id,)
        )
        material_name = c.fetchone()[0]

        # Calculate available stock
        c.execute(
            """
            SELECT COALESCE(SUM(
                CASE 
                    WHEN type IN ('IN') THEN quantity
                    WHEN type IN ('OUT') THEN -quantity
                    ELSE 0
                END
            ), 0)
            FROM transactions
            WHERE item_name = %s
            """,
            (material_name,)
        )

        available_qty = c.fetchone()[0]

        if available_qty < required_qty:
            conn.close()
            raise Exception(f"Not enough stock for {material_name}")

    # ---------------------------
    # 3. DEDUCT MATERIALS
    # ---------------------------
    for material_id, per_unit_qty in bom_items:
        required_qty = per_unit_qty * quantity

        c.execute(
            "SELECT name FROM materials WHERE id = %s",
            (material_id,)
        )
        material_name = c.fetchone()[0]

        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'OUT', %s)
            """,
            (material_name, required_qty)
        )

    # ---------------------------
    # 4. HANDLE FINISHED GOODS
    # ---------------------------
    c.execute(
        "SELECT sku FROM products WHERE id = %s",
        (product_id,)
    )
    sku = c.fetchone()[0]

    if mode == "stock":
        # Add to inventory
        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'PRODUCED', %s)
            """,
            (sku, quantity)
        )

    elif mode == "dispatch":
        # Direct dispatch (no inventory increase)
        c.execute(
            """
            INSERT INTO transactions (item_name, type, quantity)
            VALUES (%s, 'DISPATCH', %s)
            """,
            (sku, quantity)
        )

    else:
        conn.close()
        raise Exception("Invalid production mode")

    # ---------------------------
    # 5. COMMIT
    # ---------------------------
    conn.commit()
    conn.close()
