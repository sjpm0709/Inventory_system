from database.db import get_connection
from config import COLOR_MAP, BOM_RULES, EXTRA_COMPONENTS
from utils.helpers import parse_sku

def auto_generate_bom(sku):
    parsed = parse_sku(sku)
    if not parsed:
        return None

    prefix, outer, inner, base, ltype = parsed

    template = BOM_RULES.get((prefix, ltype))
    if not template:
        return None

    outer_q, inner_q, base_q = template

    bom = [
        (COLOR_MAP[outer], outer_q),
        (COLOR_MAP[inner], inner_q),
        (COLOR_MAP[base], base_q)
    ]

    for comp in EXTRA_COMPONENTS[prefix]:
        bom.append((comp, 1))

    return bom


def get_bom(sku):
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT material, quantity FROM bom WHERE sku=?", (sku,))
    data = c.fetchall()

    conn.close()

    if data:
        return data

    return auto_generate_bom(sku)