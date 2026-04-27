import streamlit as st
from database.db import init_db

from ui.materials import show_materials
from ui.stock import show_stock
from ui.dashboard import show_dashboard

init_db()

st.title("Inventory & Production System")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Materials",
    "Stock Entry"
])

if menu == "Dashboard":
    show_dashboard()

elif menu == "Materials":
    show_materials()

elif menu == "Stock Entry":
    show_stock()
