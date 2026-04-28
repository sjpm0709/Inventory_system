import streamlit as st
from services.inventory_service import add_material, get_materials, delete_material


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
        material_id, name, unit, min_stock = m

        col1, col2 = st.columns([4, 1])

        with col1:
           st.write(f"{name} ({unit}) → Min Stock: {min_stock}")

        with col2:
           if st.button("Delete", key=f"del_mat_{material_id}"):
            try:
                delete_material(material_id)
                st.success("Deleted successfully")
                st.rerun()
            except Exception as e:
                st.error(str(e))
