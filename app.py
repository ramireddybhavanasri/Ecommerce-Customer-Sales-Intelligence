
import streamlit as st
import pandas as pd

# ==================================================
# 1. PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="E-Commerce Intelligence",
    page_icon="🛒",
    layout="wide"
)

# ==================================================
# 2. CUSTOM CSS
# ==================================================

st.markdown("""
<style>

.stApp {
    background: #0B1220;
}

h1 {
    color: #38D9A9 !important;
    font-size: 38px !important;
    font-weight: 800 !important;
}

h2, h3 {
    color: #60A5FA !important;
}

[data-testid="stMetric"] {
    background: linear-gradient(135deg, #172554, #164E63);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #38BDF8;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

[data-testid="stMetricLabel"] {
    color: #BAE6FD !important;
}

[data-testid="stMetricValue"] {
    color: #FFFFFF !important;
    font-size: 30px !important;
    font-weight: bold;
}

[data-testid="stSidebar"] {
    background-color: #111C30;
}

[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# ==================================================
# 3. DASHBOARD TITLE
# ==================================================

st.title("🛒 E-Commerce Customer & Sales Intelligence")

st.write(
    "An interactive dashboard to explore e-commerce "
    "sales, customers, and business performance."
)


# ==================================================
# 4. LOAD DATASETS
# ==================================================

@st.cache_data
def load_data():

    orders = pd.read_csv("datasets/olist_orders_dataset.csv")

    customers = pd.read_csv(
        "datasets/olist_customers_dataset.csv"
    )

    order_items = pd.read_csv(
        "datasets/olist_order_items_dataset.csv"
    )

    products = pd.read_csv(
        "datasets/olist_products_dataset.csv"
    )

    payments = pd.read_csv(
        "datasets/olist_order_payments_dataset.csv"
    )

    return orders, customers, order_items, products, payments


try:
    orders, customers, order_items, products, payments = load_data()

except FileNotFoundError:
    st.error(
        "Dataset files not found. Please check your datasets folder."
    )
    st.stop()


# ==================================================
# 5. DATA PREPROCESSING
# ==================================================

orders["order_purchase_timestamp"] = pd.to_datetime(
    orders["order_purchase_timestamp"],
    errors="coerce"
)

orders["order_delivered_customer_date"] = pd.to_datetime(
    orders["order_delivered_customer_date"],
    errors="coerce"
)

orders["delivery_days"] = (
    orders["order_delivered_customer_date"]
    - orders["order_purchase_timestamp"]
).dt.days

orders["month"] = (
    orders["order_purchase_timestamp"].dt.strftime("%Y-%m")
)


# ==================================================
# 6. SIDEBAR FILTERS
# ==================================================

st.sidebar.title("Dashboard Filters")

# Order status filter

available_statuses = sorted(
    orders["order_status"].dropna().unique()
)

selected_status = st.sidebar.selectbox(
    "Select Order Status",
    ["All"] + available_statuses
)

# Date range filter

st.sidebar.subheader("Date Range Filter")

valid_dates = orders["order_purchase_timestamp"].dropna()

min_date = valid_dates.min().date()
max_date = valid_dates.max().date()

selected_dates = st.sidebar.date_input(
    "Choose Order Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date
)

# Apply filters

filtered_orders = orders.copy()

if selected_status != "All":

    filtered_orders = filtered_orders[
        filtered_orders["order_status"] == selected_status
    ]

if len(selected_dates) == 2:

    start_date, end_date = selected_dates

    filtered_orders = filtered_orders[
        (filtered_orders["order_purchase_timestamp"].dt.date >= start_date)
        & (filtered_orders["order_purchase_timestamp"].dt.date <= end_date)
    ]


# ==================================================
# 7. CREATE DASHBOARD TABS
# ==================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview",
    "Orders",
    "Customers",
    "Products",
    "Payments"
])


# ==================================================
# TAB 1: BUSINESS OVERVIEW
# ==================================================

with tab1:

    st.header("Business Overview")

    total_orders = len(filtered_orders)

    delivered_orders = (
        filtered_orders["order_status"] == "delivered"
    ).sum()

    canceled_orders = (
        filtered_orders["order_status"] == "canceled"
    ).sum()

    other_orders = (
        total_orders - delivered_orders - canceled_orders
    )

    # KPI Cards

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Total Orders",
        f"{total_orders:,}"
    )

    col2.metric(
        "Delivered Orders",
        f"{delivered_orders:,}"
    )

    col3.metric(
        "Canceled Orders",
        f"{canceled_orders:,}"
    )

    col4.metric(
        "Other Orders",
        f"{other_orders:,}"
    )

    # Order Status Chart

    st.subheader("Order Status Distribution")

    if not filtered_orders.empty:

        status_counts = (
            filtered_orders["order_status"].value_counts()
        )

        st.bar_chart(status_counts)

    else:

        st.info("No orders available for the selected filters.")


# ==================================================
# TAB 2: ORDER ANALYTICS
# ==================================================

with tab2:

    st.header("Order Analytics")

    # Monthly Order Analysis

    st.subheader("Monthly Order Analysis")

    available_months = sorted(
        filtered_orders["month"].dropna().unique()
    )

    if available_months:

        selected_month = st.selectbox(
            "Select a Month",
            available_months
        )

        monthly_orders = filtered_orders[
            filtered_orders["month"] == selected_month
        ]

        st.metric(
            "Orders in Selected Month",
            f"{len(monthly_orders):,}"
        )

        st.dataframe(
            monthly_orders.head(10),
            use_container_width=True
        )

        # Monthly Order Trend

        monthly_counts = (
            filtered_orders.groupby("month")
            .size()
            .sort_index()
        )

        st.subheader("Monthly Order Trend")

        st.line_chart(monthly_counts)

    else:

        st.info("No monthly order data available.")

    # Delivery Performance

    st.subheader("Delivery Performance")

    delivered_data = filtered_orders[
        (filtered_orders["order_status"] == "delivered")
        & (filtered_orders["delivery_days"].notna())
    ]

    if not delivered_data.empty:

        average_delivery = delivered_data["delivery_days"].mean()

        st.metric(
            "Average Delivery Time",
            f"{average_delivery:.2f} days"
        )

        # Monthly Average Delivery Time

        monthly_delivery = (
            delivered_data.groupby("month")["delivery_days"]
            .mean()
            .sort_index()
        )

        st.subheader("Monthly Average Delivery Time")

        st.line_chart(monthly_delivery)

        # Delivery Time Distribution

        delivery_counts = (
            delivered_data["delivery_days"]
            .value_counts()
            .sort_index()
        )

        st.subheader("Delivery Time Distribution")

        st.bar_chart(delivery_counts)

    else:

        st.info(
            "No delivered orders available for delivery analysis."
        )

    # Download Filtered Orders

    st.subheader("Download Order Data")

    csv_data = filtered_orders.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Filtered Orders",
        data=csv_data,
        file_name="filtered_orders.csv",
        mime="text/csv"
    )


# ==================================================
# TAB 3: CUSTOMER ANALYTICS
# ==================================================

with tab3:

    st.header("Customer Analytics")

    customer_orders = filtered_orders.merge(
        customers[["customer_id", "customer_unique_id"]],
        on="customer_id",
        how="left"
    )

    unique_customers = (
        customer_orders["customer_unique_id"].nunique()
    )

    orders_per_customer = (
        customer_orders.groupby("customer_unique_id")["order_id"]
        .count()
    )

    repeat_customers = (
        orders_per_customer > 1
    ).sum()

    # Customer KPI Cards

    col1, col2 = st.columns(2)

    col1.metric(
        "Unique Customers",
        f"{unique_customers:,}"
    )

    col2.metric(
        "Repeat Customers",
        f"{repeat_customers:,}"
    )

    # Customer Order Distribution

    st.subheader("Customer Order Distribution")

    if not orders_per_customer.empty:

        customer_distribution = (
            orders_per_customer.value_counts()
            .sort_index()
        )

        st.bar_chart(customer_distribution)

    else:

        st.info("No customer data available.")


# ==================================================
# TAB 4: PRODUCT ANALYTICS
# ==================================================

with tab4:

    st.header("Product Performance")

    # Filter order items using selected orders

    filtered_order_ids = filtered_orders["order_id"]

    filtered_items = order_items[
        order_items["order_id"].isin(filtered_order_ids)
    ]

    total_products = products["product_id"].nunique()

    # Product KPI Cards

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Unique Products",
        f"{total_products:,}"
    )

    col2.metric(
        "Products Ordered",
        f"{filtered_items['product_id'].nunique():,}"
    )

    # Merge Product Information

    product_details = filtered_items.merge(
        products[["product_id", "product_category_name"]],
        on="product_id",
        how="left"
    )

    # Top 10 Product Categories

    st.subheader("Top 10 Product Categories")

    top_categories = (
        product_details.groupby("product_category_name")["order_id"]
        .count()
        .sort_values(ascending=False)
        .head(10)
    )

    if not top_categories.empty:

        st.bar_chart(top_categories)

        st.dataframe(
            top_categories.rename("Number of Orders"),
            use_container_width=True
        )

    else:

        st.info("No product data available.")


# ==================================================
# TAB 5: PAYMENT ANALYTICS
# ==================================================

with tab5:

    st.header("Payment Analysis")

    # Filter payments using selected orders

    filtered_payments = payments[
        payments["order_id"].isin(filtered_orders["order_id"])
    ]

    total_transactions = len(filtered_payments)

    total_payment_value = (
        filtered_payments["payment_value"].sum()
    )

    # Payment KPI Cards

    col1, col2 = st.columns(2)

    col1.metric(
        "Total Transactions",
        f"{total_transactions:,}"
    )

    col2.metric(
        "Total Payment Value",
        f"R$ {total_payment_value:,.2f}"
    )

    # Payment Method Analysis

    st.subheader("Popular Payment Methods")

    payment_counts = (
        filtered_payments["payment_type"].value_counts()
    )

    if not payment_counts.empty:

        st.bar_chart(payment_counts)

    else:

        st.info("No payment data available.")

    # Payment Records

    st.subheader("Payment Records")

    st.dataframe(
        filtered_payments.head(20),
        use_container_width=True
    )


# ==================================================
# 8. FOOTER
# ==================================================

st.sidebar.divider()

st.sidebar.caption(
    "E-Commerce Customer & Sales Intelligence"
)

st.sidebar.caption(
    "Built using Python, Pandas and Streamlit"
)
