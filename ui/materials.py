import streamlit as st
from services.inventory_service import add_material, get_materials


def show_materials():
    st.header("Materials")

    name = st.text_input("Material Name")
    unit = st.selectbox("Unit", ["gms", "pcs", "mtr"])
    min_stock = st.number_input("Minimum Stock Level", min_value=0.0, value=50.0)

    if st.button("Add / Update Material"):
        if name:
            add_material(name, unit, min_stock)
            st.success("Material saved successfully")
        else:
            st.error("Material name required")

    st.subheader("Existing Materials")

    materials = get_materials()

    for m in materials:
        # m = (id, name, unit, min_stock)
        st.write(f"{m[1]} ({m[2]}) → Min Stock: {m[3]}")
