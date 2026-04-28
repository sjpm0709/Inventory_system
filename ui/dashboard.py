import streamlit as st
import pandas as pd

from services.inventory_service import get_stock, get_materials
from services.analytics_service import (
    get_weekly_material_usage,
    get_weekly_production,
    get_weekly_dispatch
)


def show_dashboard():
    st.title("Inventory Dashboard")

    raw_materials, finished_goods = get_stock()
    materials = get_materials()

    # ---------------------------
    # KPIs
    # ---------------------------
    col1, col2, col3 = st.columns(3)

    col1.metric("Raw Materials", len(raw_materials))
    col2.metric("Finished Products", len(finished_goods))
    col3.metric("Total Items", len(raw_materials) + len(finished_goods))

    st.divider()

    # ---------------------------
    # RAW MATERIAL TABLE
    # ---------------------------
    st.subheader("📦 Raw Material Stock")

    if raw_materials:
        raw_df = pd.DataFrame(
            [{"Material": k, "Stock": v} for k, v in raw_materials.items()]
        )
        st.dataframe(raw_df, use_container_width=True)
    else:
        st.info("No raw material stock")

    # ---------------------------
    # FINISHED GOODS TABLE
    # ---------------------------
    st.subheader("🏷 Finished Goods Stock")

    if finished_goods:
        fg_df = pd.DataFrame(
            [{"SKU": k, "Stock": v} for k, v in finished_goods.items()]
        )
        st.dataframe(fg_df, use_container_width=True)
    else:
        st.info("No finished goods stock")

    # ---------------------------
    # LOW STOCK ALERTS
    # ---------------------------
    st.subheader("⚠ Low Stock Alerts")

    low_stock_found = False

    material_map = {m[1]: m[3] for m in materials}  # name → min_stock

    for name, stock in raw_materials.items():
        min_stock = material_map.get(name, 0)

        if stock < min_stock:
            st.warning(f"{name} is low: {stock} (Min: {min_stock})")
            low_stock_found = True

    if not low_stock_found:
        st.success("All materials are sufficiently stocked")

    st.divider()

    # ---------------------------
    # ANALYTICS
    # ---------------------------
    st.subheader("📊 Weekly Analytics")

    # MATERIAL USAGE
    usage_data = get_weekly_material_usage()
    if usage_data:
        df = pd.DataFrame(usage_data, columns=["week", "material", "qty"])
        df = df.groupby("week")["qty"].sum().reset_index()

        st.markdown("### Raw Material Usage")
        st.line_chart(df.set_index("week"))
    else:
        st.info("No usage data")

    # PRODUCTION
    prod_data = get_weekly_production()
    if prod_data:
        df = pd.DataFrame(prod_data, columns=["week", "product", "qty"])
        df = df.groupby("week")["qty"].sum().reset_index()

        st.markdown("### Production")
        st.line_chart(df.set_index("week"))
    else:
        st.info("No production data")

    # DISPATCH
    dispatch_data = get_weekly_dispatch()
    if dispatch_data:
        df = pd.DataFrame(dispatch_data, columns=["week", "product", "qty"])
        df = df.groupby("week")["qty"].sum().reset_index()

        st.markdown("### Dispatch")
        st.line_chart(df.set_index("week"))
    else:
        st.info("No dispatch data")
