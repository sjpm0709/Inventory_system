import streamlit as st
from services.product_service import get_products
from services.inventory_service import get_materials
from services.bom_service import save_bom

def show_bom():
    st.header("BOM Management")

    products = get_products()
    product_dict = {sku: id for id, sku in products}

    selected_product = st.selectbox("Select Product", list(product_dict.keys()))

    materials = get_materials()
    material_dict = {name: id for id, name in materials}

    selected_material = st.selectbox("Material", list(material_dict.keys()))
    qty = st.number_input("Quantity per product", min_value=0.0)

    if st.button("Save BOM"):
        save_bom(product_dict[selected_product], material_dict[selected_material], qty)
        st.success("BOM Saved")
