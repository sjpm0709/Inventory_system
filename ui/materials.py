import streamlit as st
from database.db import get_connection

def show_materials():

    conn = get_connection()
    c = conn.cursor()

    st.subheader("Add Material")

    name = st.text_input("Material Name").strip().title()
    unit = st.selectbox("Unit", ["grams", "pcs"])
    cost = st.number_input("Cost per Unit", min_value=0.0)

    if st.button("Add Material"):

        if not name:
            st.error("Enter material name")
            return

        try:
            c.execute(
                "INSERT INTO materials (name, unit, cost_per_unit) VALUES (?, ?, ?)",
                (name, unit, cost)
            )
            conn.commit()
            st.success("Material Added")
        except:
            st.error("Material already exists")

    st.subheader("All Materials")

    c.execute("SELECT name, unit, cost_per_unit FROM materials")
    data = c.fetchall()

    st.dataframe(data, use_container_width=True)

    conn.close()