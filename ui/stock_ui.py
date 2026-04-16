import streamlit as st
from database.db import get_connection
from services.inventory import update_stock

def show_stock_entry():

    conn = get_connection()
    c = conn.cursor()

    st.subheader("Stock Entry")

    c.execute("SELECT name FROM materials")
    materials = [m[0] for m in c.fetchall()]

    if not materials:
        st.warning("Add materials first")
        return

    item = st.selectbox("Select Material", materials)
    qty = st.number_input("Quantity", min_value=0.0)

    if st.button("Add Stock"):

        if qty <= 0:
            st.error("Quantity must be greater than 0")
            return

        update_stock(item, qty, "IN")

        c.execute(
            "INSERT INTO transactions VALUES (NULL, datetime('now'), ?, ?, ?, ?)",
            (item, "IN", qty, "manual")
        )
        conn.commit()

        st.success(f"Stock added: {item}")

    conn.close()