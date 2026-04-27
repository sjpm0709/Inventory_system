import streamlit as st
from services.product_service import add_product, get_products

def show_products():
    st.header("Products (SKU)")

    sku = st.text_input("Enter SKU")

    if st.button("Add SKU"):
        add_product(sku)
        st.success("Product Added")

    st.subheader("Existing SKUs")

    products = get_products()
    for p in products:
        st.write(p[1])
