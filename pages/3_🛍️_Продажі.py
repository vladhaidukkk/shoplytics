import streamlit as st

from app.data import sales_data
from app.pages import sales_page, upload_page

sales_page.render()
sales_df = sales_data.session_state

# Check if sales data is uploaded.
if sales_df is None:
    st.warning(
        f"Спочатку завантажте дані продажів на сторінці '{upload_page.title}'",
        icon="⚠️",
    )
    st.stop()

# Sidebar with metrics type selector and filters.
with st.sidebar:
    metrics_type = st.radio(
        "Показувати метрики по:",
        options=["Доходам", "Прибутку", "Кількості"],
        horizontal=True,
    )

    st.subheader("Фільтри")

    date_range = st.date_input(
        "Період аналізу",
        value=(sales_df["date"].min(), sales_df["date"].max()),
        min_value=sales_df["date"].min(),
        max_value=sales_df["date"].max(),
    )

    stores = sorted(sales_df["store"].unique())
    selected_stores = st.multiselect(
        "Магазини",
        options=stores,
        default=stores,
        help="Виберіть один або декілька магазинів",
    )

    categories = sorted(sales_df["category"].unique())
    selected_categories = st.multiselect(
        "Категорії товарів",
        options=categories,
        default=categories,
        help="Виберіть одну або декілька категорій",
    )

    products = sorted(sales_df["product_name"].unique())
    selected_products = st.multiselect(
        "Товари",
        options=products,
        default=[],
        help="Виберіть конкретні товари (за замовчуванням показуються всі)",
    )

    sizes = sorted(sales_df["size"].unique())
    selected_sizes = st.multiselect(
        "Розміри",
        options=sizes,
        default=sizes,
        help="Виберіть один або декілька розмірів",
    )

    genders = sorted(sales_df["gender"].unique())
    selected_gender = st.selectbox(
        "Стать",
        options=["Всі", *genders],
        help="Виберіть стать для фільтрації",
    )

# Apply filters.
mask = (
    (sales_df["store"].isin(selected_stores))
    & (sales_df["category"].isin(selected_categories))
    & (sales_df["size"].isin(selected_sizes))
)

if date_range and len(date_range) == 2:
    mask &= sales_df["date"].dt.date >= date_range[0]
    mask &= sales_df["date"].dt.date <= date_range[1]
if selected_products:
    mask &= sales_df["product_name"].isin(selected_products)
if selected_gender != "Всі":
    mask &= sales_df["gender"] == selected_gender

filtered_df = sales_df[mask]

# Metrics tabs.
metrics_tab, charts_tab, details_tab = st.tabs(
    ["📊 Ключові метрики", "📈 Графіки", "🔍 Деталі"]
)

# Calculate profit if needed
if metrics_type == "Прибутку":
    filtered_df["profit"] = filtered_df["revenue"] - (
        filtered_df["cost"] * filtered_df["quantity"]
    )

with metrics_tab:
    col1, col2, col3, col4 = st.columns(4)

    if metrics_type == "Доходам":
        with col1:
            total_revenue = filtered_df["revenue"].sum()
            st.metric("Загальний дохід", f"{total_revenue:,.2f} ₴")

        with col2:
            avg_daily_revenue = filtered_df.groupby("date")["revenue"].sum().mean()
            st.metric("Середній дохід на день", f"{avg_daily_revenue:,.2f} ₴")

        with col3:
            avg_order_revenue = filtered_df["revenue"].mean()
            st.metric("Середній чек", f"{avg_order_revenue:,.2f} ₴")

        with col4:
            top_product = (
                filtered_df.groupby("product_name")["revenue"]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )
            st.metric("Найбільш дохідний товар", top_product)

    elif metrics_type == "Прибутку":
        with col1:
            total_profit = filtered_df["profit"].sum()
            st.metric("Загальний прибуток", f"{total_profit:,.2f} ₴")

        with col2:
            avg_daily_profit = filtered_df.groupby("date")["profit"].sum().mean()
            st.metric("Середній прибуток на день", f"{avg_daily_profit:,.2f} ₴")

        with col3:
            margin_percent = (
                filtered_df["profit"].sum() / filtered_df["revenue"].sum()
            ) * 100
            st.metric("Середня маржа", f"{margin_percent:.1f}%")

        with col4:
            top_product = (
                filtered_df.groupby("product_name")["profit"]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )
            st.metric("Найбільш прибутковий товар", top_product)

    elif metrics_type == "Кількості":
        with col1:
            total_quantity = filtered_df["quantity"].sum()
            st.metric("Загальна кількість товарів", f"{total_quantity:,}")

        with col2:
            unique_products = filtered_df["product_name"].nunique()
            st.metric("Кількість унікальних товарів", f"{unique_products:,}")

        with col3:
            avg_daily_quantity = filtered_df.groupby("date")["quantity"].sum().mean()
            st.metric("Середня кількість на день", f"{avg_daily_quantity:.1f}")

        with col4:
            top_product = (
                filtered_df.groupby("product_name")["quantity"]
                .sum()
                .sort_values(ascending=False)
                .index[0]
            )
            st.metric("Найбільш популярний товар", top_product)

with charts_tab:
    col1, col2 = st.columns(2)

    if metrics_type == "Доходам":
        st.subheader("📈 Динаміка доходів")
        daily_revenue = filtered_df.groupby("date")["revenue"].sum().reset_index()
        st.line_chart(daily_revenue.set_index("date"), use_container_width=True)

        with col1:
            st.subheader("🏆 Найбільш дохідні товари")
            top_revenue_products = (
                filtered_df.groupby("product_name")["revenue"]
                .sum()
                .sort_values(ascending=True)
                .tail(10)
            )
            st.bar_chart(top_revenue_products)

        with col2:
            st.subheader("📊 Структура доходів по категоріях")
            revenue_by_category = filtered_df.groupby("category")["revenue"].sum()
            st.bar_chart(revenue_by_category)

    elif metrics_type == "Прибутку":
        st.subheader("📈 Динаміка прибутку")
        daily_profit = filtered_df.groupby("date")["profit"].sum().reset_index()
        st.line_chart(daily_profit.set_index("date"), use_container_width=True)

        with col1:
            st.subheader("🏆 Найбільш прибуткові товари")
            top_profit_products = (
                filtered_df.groupby("product_name")["profit"]
                .sum()
                .sort_values(ascending=True)
                .tail(10)
            )
            st.bar_chart(top_profit_products)

        with col2:
            st.subheader("📊 Структура прибутку по категоріях")
            profit_by_category = filtered_df.groupby("category")["profit"].sum()
            st.bar_chart(profit_by_category)

    elif metrics_type == "Кількості":
        st.subheader("📈 Динаміка продажів")
        daily_quantity = filtered_df.groupby("date")["quantity"].sum().reset_index()
        st.line_chart(daily_quantity.set_index("date"), use_container_width=True)

        with col1:
            st.subheader("🏆 Найбільш продавані товари")
            top_quantity_products = (
                filtered_df.groupby("product_name")["quantity"]
                .sum()
                .sort_values(ascending=True)
                .tail(10)
            )
            st.bar_chart(top_quantity_products)

        with col2:
            st.subheader("📊 Розподіл продажів по категоріях")
            quantity_by_category = filtered_df.groupby("category")["quantity"].sum()
            st.bar_chart(quantity_by_category)

with details_tab:
    st.subheader("🔍 Детальна інформація")

    columns_to_show = [
        "date",
        "store",
        "product_name",
        "category",
        "size",
        "quantity",
        "price",
        "revenue",
        "cost",
    ]
    if "profit" in filtered_df.columns:
        columns_to_show.append("profit")

    st.dataframe(
        filtered_df[columns_to_show].sort_values("date", ascending=False),
        use_container_width=True,
    )

    csv = filtered_df[columns_to_show].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Експортувати", csv, "sales_analysis.csv", "text/csv")
