import streamlit as st
from services.production import produce
from services.bom import get_bom
from utils.helpers import validate_sku

def show_production():

    st.subheader("Production")

    sku = st.text_input("Enter SKU")
    qty = st.number_input("Quantity", min_value=1)

    if sku and validate_sku(sku):
        bom = get_bom(sku)
        st.write("Auto BOM:", bom)

    if st.button("Produce"):

        if not validate_sku(sku):
            st.error("Invalid SKU")
            return

        try:
            produce(sku, qty)
            st.success("Production successful")
        except Exception as e:
            st.error(str(e))