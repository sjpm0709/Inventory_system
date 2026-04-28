import streamlit as st
import pandas as pd
from services.transaction_service import get_transactions


def show_transactions():
    st.header("Transaction History")

    data = get_transactions()

    if not data:
        st.info("No transactions found")
        return

    df = pd.DataFrame(
        data,
        columns=["Item", "Type", "Quantity", "Time"]
    )

    # ---------------------------
    # FILTERS
    # ---------------------------
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:
        item_filter = st.selectbox(
            "Filter by Item",
            ["All"] + sorted(df["Item"].unique().tolist())
        )

    with col2:
        type_filter = st.selectbox(
            "Filter by Type",
            ["All"] + sorted(df["Type"].unique().tolist())
        )

    # Apply filters
    if item_filter != "All":
        df = df[df["Item"] == item_filter]

    if type_filter != "All":
        df = df[df["Type"] == type_filter]

    # ---------------------------
    # TABLE
    # ---------------------------
    st.subheader("Transactions")

    st.dataframe(df, use_container_width=True)
