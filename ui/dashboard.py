import streamlit as st
from services.inventory_service import get_stock


def show_dashboard():
    st.header("Dashboard")

    raw_materials, finished_goods = get_stock()

    # ---------------------------
    # RAW MATERIALS
    # ---------------------------
    st.subheader("Raw Materials Stock")

    if raw_materials:
        for material, qty in raw_materials.items():
            st.write(f"{material} : {qty}")
    else:
        st.info("No raw materials data available")

    # ---------------------------
    # LOW STOCK ALERT (RAW ONLY)
    # ---------------------------
    st.subheader("Low Stock Alerts (Raw Materials Only)")

    low_stock_found = False

    for material, qty in raw_materials.items():
        if qty < 50:
            st.warning(f"{material} is low: {qty}")
            low_stock_found = True

    if not low_stock_found:
        st.success("All raw materials are sufficiently stocked")

    # ---------------------------
    # FINISHED GOODS
    # ---------------------------
    st.subheader("Finished Goods Stock")

    if finished_goods:
        for sku, qty in finished_goods.items():
            st.write(f"{sku} : {qty}")
    else:
        st.info("No finished goods data available")
