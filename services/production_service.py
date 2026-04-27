from services.inventory_service import log_transaction
from services.bom_service import get_bom

def produce(sku, qty):
    bom = get_bom(sku)

    if not bom:
        raise Exception("BOM not defined")

    for material, per_unit in bom:
        log_transaction(material, per_unit * qty, "OUT")

    log_transaction(sku, qty, "IN")
