import pandas as pd
import plotly.express as px
import streamlit as st

from app.data import inventory_data, sales_data
from app.pages import inventory_page, upload_page

inventory_page.render()
inventory_df = inventory_data.session_state
sales_df = sales_data.session_state


# Check if inventory data is uploaded.
if inventory_df is None:
    st.warning(
        f"Спочатку завантажте дані складу на сторінці '{upload_page.title}'", icon="⚠️"
    )
    st.stop()

# Sidebar with filters.
with st.sidebar:
    st.subheader("Фільтри")

    stores = sorted(inventory_df["store"].unique())
    selected_stores = st.multiselect(
        "Магазини",
        options=stores,
        default=stores,
        help="Виберіть один або декілька магазинів",
    )

    categories = sorted(inventory_df["category"].unique())
    selected_categories = st.multiselect(
        "Категорії товарів",
        options=categories,
        default=categories,
        help="Виберіть одну або декілька категорій",
    )

    sizes = sorted(inventory_df["size"].unique())
    selected_sizes = st.multiselect(
        "Розміри",
        options=sizes,
        default=sizes,
        help="Виберіть один або декілька розмірів",
    )

    excess_threshold = st.slider(
        "Коефіцієнт надлишкового запасу",
        min_value=1.0,
        max_value=5.0,
        value=3.0,
        step=0.5,
        help="Товари з запасом більше ніж (коеф. × мін. к-сть) вважаються надлишковими",
    )

    dead_stock_days = st.slider(
        "Період неактивності (днів)",
        min_value=30,
        max_value=180,
        value=30,
        step=30,
        help="Товари без продажів протягом цього періоду вважаються мертвим складом",
    )

# Apply filters.
mask = (
    (inventory_df["store"].isin(selected_stores))
    & (inventory_df["category"].isin(selected_categories))
    & (inventory_df["size"].isin(selected_sizes))
)

filtered_df = inventory_df[mask]

# Calculate KPIs.
st.subheader("📊 Ключові метрики")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

# Calculate base metrics
total_sku = filtered_df["product_id"].nunique()
total_items = filtered_df["stock_qty"].sum()

with kpi1:
    st.metric("Загальна к-сть SKU", f"{total_sku:,}")

with kpi2:
    low_stock_mask = filtered_df["stock_qty"] < filtered_df["min_qty"]
    low_stock = filtered_df[low_stock_mask].shape[0]
    st.metric("Низький запас", f"{low_stock:,}")

with kpi3:
    zero_stock = filtered_df[filtered_df["stock_qty"] == 0].shape[0]
    st.metric("Нульовий запас", f"{zero_stock:,}")

with kpi4:
    excess_mask = filtered_df["stock_qty"] > (filtered_df["min_qty"] * excess_threshold)
    excess_stock = filtered_df[excess_mask].shape[0]
    st.metric("Надлишковий запас", f"{excess_stock:,}")

with kpi5:
    to_order_mask = (filtered_df["stock_qty"] <= filtered_df["min_qty"]) & (
        filtered_df["stock_qty"] > 0
    )
    to_order = filtered_df[to_order_mask].shape[0]
    st.metric("До замовлення", f"{to_order:,}")


# Create tabs for different views.
stock_level_tab, low_stock_tab, dead_stock_tab, table_tab = st.tabs(
    [
        "📉 Рівень залишків",
        "🧯 Низький запас",
        "🧊 Мертвий склад",
        "🔍 Детальна таблиця",
    ]
)


def color_status(row):
    if row["stock_qty"] == 0:
        return ["background-color: #ffcccc" for _ in row]  # Red
    elif row["stock_qty"] < row["min_qty"]:
        return ["background-color: #fff3cd" for _ in row]  # Yellow
    return ["background-color: #d1e7dd" for _ in row]  # Green


with stock_level_tab:
    st.subheader("📉 Рівень залишків по категоріях")

    stock_by_cat = (
        filtered_df.groupby(["category", "store"])["stock_qty"].sum().reset_index()
    )
    total_by_cat = (
        stock_by_cat.groupby("category")["stock_qty"]
        .sum()
        .reset_index()
        .rename(columns={"stock_qty": "total"})
    )
    stock_by_cat = stock_by_cat.merge(total_by_cat, on="category")

    chart_labels = {
        "category": "Категорія",
        "stock_qty": "Кількість",
        "store": "Магазин",
    }
    fig = px.bar(
        stock_by_cat,
        x="category",
        y="stock_qty",
        color="store",
        labels=chart_labels,
        text="stock_qty",
    )

    for cat in total_by_cat["category"].unique():
        total = total_by_cat[total_by_cat["category"] == cat]["total"].iloc[0]
        fig.add_annotation(
            x=cat,
            y=total,
            text=f"Всього: {total:,}",
            showarrow=False,
            yshift=10,
        )

    fig.update_traces(textposition="inside")
    st.plotly_chart(fig, use_container_width=True)

with low_stock_tab:
    st.subheader("🧯 Товари з низьким запасом")

    low_stock_df = filtered_df[filtered_df["stock_qty"] < filtered_df["min_qty"]]
    if not low_stock_df.empty:
        styled_df = low_stock_df[
            ["product_name", "store", "category", "stock_qty", "min_qty"]
        ].style.apply(color_status, axis=1)

        st.dataframe(
            styled_df,
            column_config={
                "product_name": "Назва",
                "store": "Магазин",
                "category": "Категорія",
                "stock_qty": st.column_config.NumberColumn(
                    "Поточний", help="Поточна кількість на складі"
                ),
                "min_qty": st.column_config.NumberColumn(
                    "Мінімум", help="Мінімальна необхідна кількість"
                ),
            },
            height=400,
        )
    else:
        st.info("Немає товарів з низьким запасом", icon="ℹ️")

with dead_stock_tab:
    st.subheader("🧊 Мертвий склад")

    if sales_df is not None:
        last_sale_date = (
            sales_df.groupby(["store", "product_id"])["date"]
            .max()
            .reset_index()
            .rename(columns={"date": "last_sale_date"})
        )

        dead_stock_df = filtered_df.merge(
            last_sale_date, on=["store", "product_id"], how="left"
        )

        dead_stock_threshold = pd.Timestamp("now") - pd.Timedelta(days=dead_stock_days)
        dead_stock_mask = (
            (dead_stock_df["last_sale_date"] < dead_stock_threshold)
            | (dead_stock_df["last_sale_date"].isna())
        ) & (dead_stock_df["stock_qty"] > dead_stock_df["min_qty"] * excess_threshold)

        dead_stock_items = dead_stock_df[dead_stock_mask].sort_values(
            "stock_qty", ascending=False
        )

        if not dead_stock_items.empty:
            st.dataframe(
                dead_stock_items[
                    ["product_name", "store", "stock_qty", "last_sale_date"]
                ],
                column_config={
                    "product_name": "Назва",
                    "store": "Магазин",
                    "stock_qty": "Залишок",
                    "last_sale_date": st.column_config.DatetimeColumn(
                        "Дата продажу", format="DD.MM.YYYY"
                    ),
                },
                height=400,
            )
        else:
            st.info("Немає товарів із надлишковим запасом", icon="ℹ️")
    else:
        st.warning("Для аналізу мертвого складу потрібні дані продажів", icon="⚠️")

with table_tab:
    st.subheader("📋 Повна таблиця складських запасів")

    columns = ["product_name", "category", "size", "stock_qty", "min_qty", "store"]

    styled_df = filtered_df[columns].style.apply(color_status, axis=1)

    with st.expander("ℹ️ Кольорове позначення статусів"):
        st.markdown(
            """
            - 🔴 **Червоний** - Товар відсутній на складі (нульовий запас)
            - 🟡 **Жовтий** - Низький запас (менше мінімальної кількості)
            - 🟢 **Зелений** - Нормальний рівень запасу
            """
        )

    st.dataframe(
        styled_df,
        column_config={
            "product_name": "Товар",
            "category": "Категорія",
            "size": "Розмір",
            "stock_qty": "Запас",
            "min_qty": "Мін. запас",
            "store": "Магазин",
        },
        height=600,
    )

    csv = filtered_df[columns].to_csv(index=False).encode("utf-8")
    st.download_button("📥 Експортувати", csv, "inventory_export.csv", "text/csv")
