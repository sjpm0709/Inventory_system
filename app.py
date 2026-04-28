import streamlit as st
import os

from database.db import init_db

# UI imports
from ui.materials import show_materials
from ui.stock import show_stock_entry
from ui.dashboard import show_dashboard
from ui.products import show_products
from ui.bom import show_bom
from ui.production import show_production
from ui.transactions import show_transactions


# -----------------------------
# DB INIT (safe for cloud)
# -----------------------------
if not os.path.exists("inventory_v2.db"):
    init_db()


# -----------------------------
# APP UI
# -----------------------------
st.set_page_config(page_title="Inventory System", layout="wide")

st.title("Inventory & Production System")


# -----------------------------
# SIDEBAR MENU
# -----------------------------
menu = st.sidebar.selectbox(
    "Menu",
    [
        "Dashboard",
        "Materials",
        "Stock Entry",
        "Products",
        "BOM",
        "Production",
        "Transactions"
    ]
)


# -----------------------------
# ROUTING
# -----------------------------
if menu == "Dashboard":
    show_dashboard()

elif menu == "Materials":
    show_materials()

elif menu == "Stock Entry":
    show_stock_entry()

elif menu == "Products":
    show_products()

elif menu == "BOM":
    show_bom()

elif menu == "Production":
    show_production()

elif menu == "Transactions":
    show_transactions()
