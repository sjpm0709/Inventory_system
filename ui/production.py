import streamlit as st
from services.product_service import get_products
from services.production_service import produce, dispatch_product
from services.inventory_service import get_stock
from services.bom_service import get_bom


def show_production():
    st.header("Production")

    products = get_products()

    if not products:
        st.warning("No products available")
        return

    product_dict = {sku: id for id, sku, name in products}

    raw_materials, finished_goods = get_stock()

    # ===========================
    # 🔹 PRODUCTION SECTION
    # ===========================
    st.subheader("Produce Product")

    selected_sku = st.selectbox("Select Product", list(product_dict.keys()))
    product_id = product_dict[selected_sku]

    quantity = st.number_input("Quantity to Produce", min_value=1, step=1)

    # ---------------------------
    # SHOW BOM REQUIREMENTS
    # ---------------------------
    st.markdown("### Material Requirements")
    st.info("Required vs available materials before production")

    bom_items = get_bom(product_id)

    if not bom_items:
        st.warning("No BOM defined for this product")
    else:
        for _, material_name, per_unit_qty in bom_items:
            required = float(per_unit_qty) * float(quantity)
            available = float(raw_materials.get(material_name, 0))

            if available >= required:
                status = "✅ OK"
            else:
                shortage = required - available
                status = f"❌ SHORT by {round(shortage, 2)}"

            st.write(
                f"{material_name} → Required: {round(required,2)} | Available: {round(available,2)} {status}"
            )

    # ---------------------------
    # MODE
    # ---------------------------
    mode = st.radio(
        "Production Output",
        ["Add to Inventory", "Direct Dispatch"]
    )

    mode_value = "stock" if mode == "Add to Inventory" else "dispatch"

    if st.button("Run Production", key="produce_btn"):
        try:
            produce(product_id, quantity, mode_value)
            st.success("Production completed successfully")
        except Exception as e:
            st.error(str(e))

    st.divider()

    # ===========================
    # 🔹 DISPATCH SECTION
    # ===========================
    st.subheader("Dispatch from Inventory")

    selected_dispatch_sku = st.selectbox(
        "Select Product to Dispatch",
        list(product_dict.keys()),
        key="dispatch_product"
    )

    dispatch_qty = st.number_input(
        "Dispatch Quantity",
        min_value=1,
        step=1,
        key="dispatch_qty"
    )

    # ---------------------------
    # SHOW CURRENT STOCK
    # ---------------------------
    current_stock = float(finished_goods.get(selected_dispatch_sku, 0))

    st.info(f"Current Stock: {round(current_stock,2)}")

    if dispatch_qty > current_stock:
        st.warning("⚠ Dispatch quantity exceeds available stock")

    if st.button("Dispatch Product", key="dispatch_btn"):
        try:
            dispatch_product(
                product_dict[selected_dispatch_sku],
                dispatch_qty
            )
            st.success("Product dispatched successfully")
        except Exception as e:
            st.error(str(e))
