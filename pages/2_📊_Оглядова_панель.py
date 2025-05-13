import pandas as pd
import plotly.express as px
import streamlit as st

from app.data import customers_data, inventory_data, sales_data
from app.pages import dashboard_page, upload_page

dashboard_page.render()

# Load all datasets
sales_df = sales_data.session_state
inventory_df = inventory_data.session_state
customers_df = customers_data.session_state

# Check if required data is uploaded
if sales_df is None:
    st.warning(
        f"Спочатку завантажте дані продажів на сторінці '{upload_page.title}'",
        icon="⚠️",
    )
    st.stop()

# Sidebar filters
with st.sidebar:
    st.subheader("Фільтри")

    # Date range filter
    date_range = st.date_input(
        "Період аналізу",
        value=(sales_df["date"].min(), sales_df["date"].max()),
        min_value=sales_df["date"].min(),
        max_value=sales_df["date"].max(),
    )

    # Store filter
    stores = sorted(sales_df["store"].unique())
    selected_store = st.selectbox(
        "Магазин",
        options=["Всі", *stores],
        help="Виберіть магазин для фільтрації",
    )

# Apply filters to sales data
mask = pd.Series(True, index=sales_df.index)

if date_range and len(date_range) == 2:
    mask &= sales_df["date"].dt.date.between(date_range[0], date_range[1])

if selected_store != "Всі":
    mask &= sales_df["store"] == selected_store

filtered_sales_df = sales_df[mask]

# Filter inventory and customers data by store if selected
if inventory_df is not None:
    if selected_store != "Всі":
        filtered_inventory_df = inventory_df[inventory_df["store"] == selected_store]
    else:
        filtered_inventory_df = inventory_df

if customers_df is not None:
    if selected_store != "Всі":
        filtered_customers_df = customers_df[customers_df["store"] == selected_store]
    else:
        filtered_customers_df = customers_df

# Calculate KPIs
st.subheader("📊 Ключові метрики")

# Create three rows of metrics
sales_metrics, inventory_metrics, customer_metrics = st.tabs(
    ["🛍️ Продажі", "📦 Склад", "👥 Клієнти"]
)

with sales_metrics:
    kpi1, kpi2, kpi3 = st.columns(3)

    with kpi1:
        total_revenue = filtered_sales_df["revenue"].sum()
        st.metric("Загальний виторг", f"{total_revenue:,.2f} ₴")

    with kpi2:
        avg_check = (
            filtered_sales_df.groupby(["date", "store"])["revenue"].mean().mean()
        )
        st.metric("Середній чек", f"{avg_check:,.2f} ₴")

    with kpi3:
        total_costs = (filtered_sales_df["cost"] * filtered_sales_df["quantity"]).sum()
        gross_profit = filtered_sales_df["revenue"].sum() - total_costs
        st.metric("Валовий прибуток", f"{gross_profit:,.2f} ₴")

with inventory_metrics:
    if inventory_df is not None:
        kpi4, kpi5, kpi6 = st.columns(3)

        with kpi4:
            total_items = filtered_inventory_df["stock_qty"].sum()
            st.metric("Загальна кількість", f"{total_items:,}")

        with kpi5:
            low_stock = filtered_inventory_df[
                filtered_inventory_df["stock_qty"] < filtered_inventory_df["min_qty"]
            ].shape[0]
            st.metric("Товари з низьким запасом", f"{low_stock:,}")

        with kpi6:
            out_of_stock = filtered_inventory_df[
                filtered_inventory_df["stock_qty"] == 0
            ].shape[0]
            st.metric("Відсутні товари", f"{out_of_stock:,}")
    else:
        st.info("Завантажте дані про складські запаси для перегляду метрик", icon="ℹ️")

with customer_metrics:
    if customers_df is not None:
        kpi7, kpi8, kpi9 = st.columns(3)

        with kpi7:
            total_customers = len(filtered_customers_df)
            st.metric("Всього клієнтів", f"{total_customers:,}")

        with kpi8:
            avg_customer_value = filtered_customers_df["total_spent"].mean()
            st.metric("Середня цінність клієнта", f"{avg_customer_value:,.2f} ₴")

        with kpi9:
            loyal_customers = (filtered_customers_df["total_orders"] > 1).sum()
            loyal_percent = (loyal_customers / total_customers) * 100
            st.metric("Постійні клієнти", f"{loyal_percent:.1f}%")
    else:
        st.info("Завантажте дані про клієнтів для перегляду метрик", icon="ℹ️")

# Visual analytics section
st.subheader("📈 Динаміка та структура продажів")

# Line chart: Sales over time
daily_sales = filtered_sales_df.groupby("date")["revenue"].sum().reset_index()
fig_timeline = px.line(
    daily_sales,
    x="date",
    y="revenue",
    title="Динаміка продажів по днях",
    labels={"date": "Дата", "revenue": "Виторг, ₴"},
)
st.plotly_chart(fig_timeline, use_container_width=True)

# Create two columns for the remaining charts
col1, col2 = st.columns(2)

with col1:
    # Bar chart: Sales by store
    sales_by_store = filtered_sales_df.groupby("store")["revenue"].sum().reset_index()
    fig_stores = px.bar(
        sales_by_store,
        x="store",
        y="revenue",
        title="Порівняння продажів по магазинах",
        labels={"store": "Магазин", "revenue": "Виторг, ₴"},
    )
    st.plotly_chart(fig_stores, use_container_width=True)

with col2:
    # Pie chart: Sales by category
    sales_by_category = filtered_sales_df.groupby("category")["revenue"].sum()
    fig_categories = px.pie(
        values=sales_by_category.values,
        names=sales_by_category.index,
        title="Розподіл продажів по категоріях товарів",
    )
    st.plotly_chart(fig_categories, use_container_width=True)
