import streamlit as st
from services.product_service import get_products
from services.production_service import produce
from services.production_service import produce, dispatch_product

def show_production():
    st.header("Production")

    # ---------------------------
    # FETCH PRODUCTS
    # ---------------------------
    products = get_products()

    if not products:
        st.warning("No products available")
        return

    st.subheader("Dispatch from Inventory")

products = get_products()
product_dict = {sku: id for id, sku, name in products}

selected_dispatch_product = st.selectbox(
    "Select Product to Dispatch", list(product_dict.keys()), key="dispatch"
)

dispatch_qty = st.number_input(
    "Dispatch Quantity", min_value=1, step=1, key="dispatch_qty"
)

if st.button("Dispatch Product"):
    try:
        dispatch_product(product_dict[selected_dispatch_product], dispatch_qty)
        st.success("Product dispatched successfully")
    except Exception as e:
        st.error(str(e))

    # products = (id, sku, name)
    product_dict = {sku: id for id, sku, name in products}

    selected_sku = st.selectbox("Select Product", list(product_dict.keys()))
    product_id = product_dict[selected_sku]

    # ---------------------------
    # QUANTITY INPUT
    # ---------------------------
    quantity = st.number_input("Quantity to Produce", min_value=1, step=1)

    # ---------------------------
    # MODE SELECTION (IMPORTANT)
    # ---------------------------
    mode = st.radio(
        "Production Output",
        ["Add to Inventory", "Direct Dispatch"]
    )

    # Map UI → backend value
    mode_value = "stock" if mode == "Add to Inventory" else "dispatch"

    # ---------------------------
    # PRODUCE BUTTON
    # ---------------------------
    if st.button("Run Production"):
        try:
            produce(product_id, quantity, mode_value)
            st.success("Production completed successfully")
        except Exception as e:
            st.error(str(e))
