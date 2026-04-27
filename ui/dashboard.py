import streamlit as st
from services.inventory_service import get_stock

def show_dashboard():
    st.header("Dashboard")

    stock = get_stock()

    st.subheader("Current Stock")
    st.write(stock)

    st.subheader("Low Stock")
    for k, v in stock.items():
        if v < 50:
            st.warning(f"{k} is low: {v}")
