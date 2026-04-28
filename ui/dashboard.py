import streamlit as st
import pandas as pd
from services.inventory_service import get_stock, get_materials


def show_dashboard():
    st.title("Inventory Dashboard")

    raw_materials, finished_goods = get_stock()
    materials = get_materials()

    # ---------------------------
    # PREP DATA
    # ---------------------------
    threshold_map = {name: min_stock for _, name, _, min_stock in materials}

    raw_data = []
    for name, qty in raw_materials.items():
        raw_data.append({
            "Material": name,
            "Stock": qty,
            "Min Stock": threshold_map.get(name, 50)
        })

    raw_df = pd.DataFrame(raw_data)

    fg_data = []
    for sku, qty in finished_goods.items():
        fg_data.append({
            "Product SKU": sku,
            "Stock": qty
        })

    fg_df = pd.DataFrame(fg_data)

    # ---------------------------
    # KPI CARDS
    # ---------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Total Raw Materials", len(raw_materials))
    col2.metric("Total SKUs", len(finished_goods))
    col3.metric("Total Inventory Items", len(raw_materials) + len(finished_goods))

    st.divider()

    # ---------------------------
    # RAW MATERIALS TABLE
    # ---------------------------
    st.subheader("Raw Materials")

    if not raw_df.empty:
        st.dataframe(raw_df, use_container_width=True)
    else:
        st.info("No raw material data")

    # ---------------------------
    # ALERTS
    # ---------------------------
    st.subheader("Stock Alerts")

    alert_found = False

    for _, row in raw_df.iterrows():
        if row["Stock"] < row["Min Stock"]:
            st.error(f"{row['Material']} LOW → {row['Stock']} (Min: {row['Min Stock']})")
            alert_found = True
        elif row["Stock"] < row["Min Stock"] * 1.2:
            st.warning(f"{row['Material']} Getting Low → {row['Stock']}")

    if not alert_found:
        st.success("All materials healthy")

    st.divider()

    # ---------------------------
    # FINISHED GOODS
    # ---------------------------
    st.subheader("Finished Goods")

    if not fg_df.empty:
        st.dataframe(fg_df, use_container_width=True)
    else:
        st.info("No finished goods data")
