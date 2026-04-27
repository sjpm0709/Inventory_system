import streamlit as st
import os

from database.db import init_db

# UI imports
from ui.materials import show_materials
from ui.stock import show_stock
from ui.dashboard import show_dashboard
from ui.products import show_products
from ui.bom import show_bom
from ui.production import show_production


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
        "Production"
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
    show_stock()

elif menu == "Products":
    show_products()

elif menu == "BOM":
    show_bom()

elif menu == "Production":
    show_production()
import streamlit as st
import psycopg2

st.title("DB Connection Test")

try:
    conn = psycopg2.connect(
        host=st.secrets["DB_HOST"],
        database=st.secrets["DB_NAME"],
        user=st.secrets["DB_USER"],
        password=st.secrets["DB_PASSWORD"],
        port=st.secrets["DB_PORT"],
        sslmode="require",
        connect_timeout=10
    )
    
    st.success("✅ Connected to Supabase successfully")

    cur = conn.cursor()
    cur.execute("SELECT 1;")
    result = cur.fetchone()
    
    st.write("Test query result:", result)

except Exception as e:
    st.error(f"❌ ERROR: {e}")
