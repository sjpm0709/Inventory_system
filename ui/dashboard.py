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
    # ANALYTICS SECTION
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
