def parse_sku(sku):
    try:
        prefix, code = sku.split("-")
        return prefix, code[0], code[1], code[2], code[3]
    except:
        return None

def validate_sku(sku):
    data = parse_sku(sku)
    return data is not None