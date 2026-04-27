import streamlit as st
from services.inventory_service import add_material

def show_materials():
    st.header("Add Material")

    name = st.text_input("Material Name")
    unit = st.selectbox("Unit", ["grams", "pcs"])

    if st.button("Add"):
        add_material(name, unit)
        st.success("Material Added")
