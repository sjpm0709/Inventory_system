from database.db import get_connection


def get_weekly_material_usage():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            DATE_TRUNC('week', created_at) AS week,
            item_name,
            SUM(quantity) as total_used
        FROM transactions
        WHERE type = 'OUT'
        GROUP BY week, item_name
        ORDER BY week
    """)

    data = c.fetchall()
    conn.close()
    return data


def get_weekly_production():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            DATE_TRUNC('week', created_at) AS week,
            item_name,
            SUM(quantity) as total_produced
        FROM transactions
        WHERE type = 'PRODUCED'
        GROUP BY week, item_name
        ORDER BY week
    """)

    data = c.fetchall()
    conn.close()
    return data


def get_weekly_dispatch():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        SELECT
            DATE_TRUNC('week', created_at) AS week,
            item_name,
            SUM(quantity) as total_dispatched
        FROM transactions
        WHERE type = 'DISPATCH'
        GROUP BY week, item_name
        ORDER BY week
    """)

    data = c.fetchall()
    conn.close()
    return data
