import streamlit as st
from database.models import init_db

from ui.dashboard import show_dashboard
from ui.materials import show_materials
from ui.stock_ui import show_stock_entry
from ui.production_ui import show_production
from ui.bom_ui import show_bom
from ui.logs_ui import show_logs

init_db()

st.title("Inventory System")

menu = st.sidebar.selectbox("Menu", [
    "Dashboard",
    "Materials",
    "Stock Entry",
    "Production",
    "BOM Management",
    "Logs"
])

if menu == "Dashboard":
    show_dashboard()

elif menu == "Materials":
    show_materials()

elif menu == "Stock Entry":
    show_stock_entry()

elif menu == "Production":
    show_production()

elif menu == "BOM Management":
    show_bom()

elif menu == "Logs":
    show_logs()