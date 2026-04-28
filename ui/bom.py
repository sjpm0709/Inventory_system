import streamlit as st
from services.product_service import get_products
from services.inventory_service import get_materials
from services.bom_service import save_bom


def show_bom():
    st.header("BOM Management")

    # ---------------------------
    # PRODUCTS
    # ---------------------------
    products = get_products()
    product_dict = {sku: id for id, sku, name in products}

    selected_product = st.selectbox("Select Product", list(product_dict.keys()))

    # ---------------------------
    # MATERIALS
    # ---------------------------
    materials = get_materials()

    st.subheader("Define Materials for Product")

    bom_data = []

    for m in materials:
        material_id, name, unit, min_stock = m

        qty = st.number_input(
            f"{name} ({unit})",
            min_value=0.0,
            key=f"bom_{material_id}"
        )

        if qty > 0:
            bom_data.append((material_id, qty))

    # ---------------------------
    # SAVE BOM
    # ---------------------------
    if st.button("Save BOM"):
        if not bom_data:
            st.error("Add at least one material")
            return

        save_bom(product_dict[selected_product], bom_data)
        st.success("BOM saved successfully")
