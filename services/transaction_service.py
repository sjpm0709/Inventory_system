from database.db import get_connection


def get_transactions():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT item_name, type, quantity, created_at
        FROM transactions
        ORDER BY created_at DESC
    """)

    data = c.fetchall()
    conn.close()
    return data
