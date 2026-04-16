import streamlit as st
import pandas as pd
from database.db import get_connection

def show_bom():

    conn = get_connection()
    c = conn.cursor()

    st.subheader("BOM Management")

    sku = st.text_input("Enter SKU")

    if not sku:
        return

    c.execute("SELECT material, quantity FROM bom WHERE sku=?", (sku,))
    data = c.fetchall()

    df = pd.DataFrame(data, columns=["Material", "Quantity"])

    # Get materials list
    c.execute("SELECT name FROM materials")
    material_list = [m[0] for m in c.fetchall()]

    edited_df = st.data_editor(
        df,
        column_config={
            "Material": st.column_config.SelectboxColumn(
                "Material",
                options=material_list
            )
        },
        num_rows="dynamic",
        use_container_width=True
    )

    if st.button("Save BOM"):

        c.execute("DELETE FROM bom WHERE sku=?", (sku,))

        for _, row in edited_df.iterrows():
            if row["Material"] and row["Quantity"] > 0:
                c.execute(
                    "INSERT INTO bom VALUES (?, ?, ?)",
                    (sku, row["Material"], row["Quantity"])
                )

        conn.commit()
        st.success("BOM Saved")

    conn.close()