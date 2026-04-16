import streamlit as st
import pandas as pd
from database.db import get_connection

def show_logs():

    conn = get_connection()
    c = conn.cursor()

    st.subheader("Transaction Logs")

    c.execute("SELECT * FROM transactions ORDER BY date DESC")
    data = c.fetchall()

    df = pd.DataFrame(data, columns=[
        "ID", "Date", "Item", "Type", "Quantity", "Source"
    ])

    st.dataframe(df, use_container_width=True)

    conn.close()