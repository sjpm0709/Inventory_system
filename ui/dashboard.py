import streamlit as st
import pandas as pd
from services.inventory import get_stock
from database.db import get_connection

def show_dashboard():

    st.subheader("Inventory Dashboard")

    stock = get_stock()
    df = pd.DataFrame(stock.items(), columns=["Item", "Stock"])

    st.dataframe(df, use_container_width=True)

    # Low stock
    low = df[df["Stock"] < 50]
    st.subheader("Low Stock Alert")
    st.dataframe(low, use_container_width=True)

    # Inventory Value
    conn = get_connection()
    c = conn.cursor()

    c.execute("SELECT name, cost_per_unit FROM materials")
    cost_map = dict(c.fetchall())

    total_value = 0
    for item, qty in stock.items():
        total_value += qty * cost_map.get(item, 0)

    st.subheader("Total Inventory Value")
    st.write(f"₹ {round(total_value, 2)}")

    conn.close()