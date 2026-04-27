from services.inventory_service import log_transaction
from services.bom_service import get_bom

def produce(product_id, sku, qty):
    bom = get_bom(product_id)

    if not bom:
        raise Exception("No BOM found")

    for material, per_unit in bom:
        log_transaction(material, per_unit * qty, "OUT")

    log_transaction(sku, qty, "IN")
