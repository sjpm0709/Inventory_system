import streamlit as st
from services.inventory_service import get_materials, log_transaction

def show_stock():
    st.header("Stock Entry")

    materials = get_materials()
    material_dict = {name: id for id, name in materials}

    selected = st.selectbox("Material", list(material_dict.keys()))
    qty = st.number_input("Quantity", min_value=0.0)

    ttype = st.selectbox("Type", ["IN", "OUT"])

    if st.button("Submit"):
        log_transaction(selected, qty, ttype)
        st.success("Stock Updated")
