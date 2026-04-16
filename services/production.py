from services.inventory import update_stock, get_stock
from services.bom import get_bom
from database.db import get_connection
from datetime import datetime

def produce(sku, qty):

    materials = get_bom(sku)
    if not materials:
        raise Exception("Invalid SKU or BOM missing")

    stock = get_stock()

    # Validate
    for m, q in materials:
        if stock.get(m, 0) < q * qty:
            raise Exception(f"Insufficient stock: {m}")

    # Deduct
    for m, q in materials:
        update_stock(m, q * qty, "OUT")

    # Add product
    update_stock(sku, qty, "IN")

    # Log
    conn = get_connection()
    c = conn.cursor()

    for m, q in materials:
        c.execute(
            "INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?, ?)",
            (datetime.now(), m, "OUT", q * qty, "production")
        )

    c.execute(
        "INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?, ?)",
        (datetime.now(), sku, "IN", qty, "production")
    )

    conn.commit()
    conn.close()