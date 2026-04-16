from database.db import get_connection

def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Materials
    c.execute("""
    CREATE TABLE IF NOT EXISTS materials (
        name TEXT PRIMARY KEY,
        unit TEXT,
        cost_per_unit REAL
    )
    """)

    # Stock
    c.execute("""
    CREATE TABLE IF NOT EXISTS stock (
        item_name TEXT PRIMARY KEY,
        quantity REAL
    )
    """)

    # BOM
    c.execute("""
    CREATE TABLE IF NOT EXISTS bom (
        sku TEXT,
        material TEXT,
        quantity REAL
    )
    """)

    # Transactions
    c.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        item TEXT,
        type TEXT,
        quantity REAL,
        source TEXT
    )
    """)

    conn.commit()
    conn.close()