import streamlit as st
from services.product_service import get_products
from services.inventory_service import produce

def show_production():
    st.header("Production")

    products = get_products()
    product_dict = {sku: id for id, sku, name in products}

    if not product_dict:
        st.warning("No products found. Add products first.")
        return

    selected_product = st.selectbox("Select SKU", list(product_dict.keys()))
    qty = st.number_input("Quantity to Produce", min_value=1)

    if st.button("Produce"):
        try:
            produce(product_dict[selected_product], selected_product, qty)
            st.success("Production Completed")
        except Exception as e:
            st.error(str(e))
