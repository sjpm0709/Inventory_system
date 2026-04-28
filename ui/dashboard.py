import streamlit as st
import pandas as pd

from services.inventory_service import get_stock, get_materials
from services.analytics_service import (
    get_weekly_material_usage,
    get_weekly_production,
    get_weekly_dispatch
)


def show_dashboard():
    st.title("Haydn Inventory Management")

    raw_materials, finished_goods = get_stock()
    materials = get_materials()

    # ---------------------------
    # KPI CALCULATIONS
    # ---------------------------
    
    total_finished_stock = sum(finished_goods.values())

    # analytics totals
    production_data = get_weekly_production()
    dispatch_data = get_weekly_dispatch()

    total_produced = sum([row[2] for row in production_data]) if production_data else 0
    total_dispatched = sum([row[2] for row in dispatch_data]) if dispatch_data else 0

    # ---------------------------
    # KPI ROW 1 (COUNTS)
    # ---------------------------
    raw_material_count = len(raw_materials)
    finished_sku_count = len(finished_goods)

    col1, col2, col3 = st.columns(3)

    col1.metric("Material Types", raw_material_count)
    col2.metric("Product SKUs", finished_sku_count)
    col3.metric("Total Dispatched", round(total_dispatched, 2))


    # ---------------------------
    # KPI ROW 2 (QUANTITIES)
    # ---------------------------
    total_raw_units = sum(raw_materials.values())
    total_finished_stock = sum(finished_goods.values())

    col4, col5, col6 = st.columns(3)

    
    col5.metric("Finished Stock Units", round(total_finished_stock, 2))
    col6.metric("Total Produced", round(total_produced, 2))
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

    material_map = {m[1]: m[3] for m in materials}  # name → min_stock
    low_found = False

    for name, stock in raw_materials.items():
        min_stock = material_map.get(name, 0)

        if stock < min_stock:
            st.warning(f"{name} is low: {stock} (Min: {min_stock})")
            low_found = True

    if not low_found:
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
    if production_data:
        df = pd.DataFrame(production_data, columns=["week", "product", "qty"])
        df = df.groupby("week")["qty"].sum().reset_index()

        st.markdown("### Production")
        st.line_chart(df.set_index("week"))
    else:
        st.info("No production data")

    # DISPATCH
    if dispatch_data:
        df = pd.DataFrame(dispatch_data, columns=["week", "product", "qty"])
        df = df.groupby("week")["qty"].sum().reset_index()

        st.markdown("### Dispatch")
        st.line_chart(df.set_index("week"))
    else:
        st.info("No dispatch data")
