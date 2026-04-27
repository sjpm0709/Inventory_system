import streamlit as st
from services.inventory_service import add_transaction, get_materials


def show_stock_entry():
    st.subheader("Stock Entry")

    materials = get_materials()

    if not materials:
        st.warning("No materials found. Add materials first.")
        return

    material_names = [m[1] for m in materials]

    selected_material = st.selectbox("Select Material", material_names)

    transaction_type = st.selectbox("Type", ["IN", "OUT"])

    quantity = st.number_input("Quantity", min_value=0.0, step=1.0)

    if st.button("Submit"):
        if quantity <= 0:
            st.error("Quantity must be greater than 0")
            return

        add_transaction(selected_material, transaction_type, quantity)
        st.success("Stock updated successfully")
