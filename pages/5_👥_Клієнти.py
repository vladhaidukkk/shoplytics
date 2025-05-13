from datetime import datetime, timedelta

import pandas as pd
import plotly.express as px
import streamlit as st

from app.data import customers_data, sales_data
from app.pages import customers_page, upload_page

customers_page.render()
customers_df = customers_data.session_state
sales_df = sales_data.session_state

if customers_df is None:
    st.warning(
        f"Спочатку завантажте дані про клієнтів на сторінці '{upload_page.title}'",
        icon="⚠️",
    )
    st.stop()

with st.sidebar:
    st.subheader("Фільтри")

    stores = sorted(customers_df["store"].unique())
    selected_stores = st.multiselect(
        "Магазини",
        options=stores,
        default=stores,
        help="Виберіть один або декілька магазинів",
    )

    genders = sorted(customers_df["gender"].unique())
    selected_gender = st.selectbox(
        "Стать", options=["Всі", *genders], help="Виберіть стать для фільтрації"
    )

    age_min = int(customers_df["age"].min())
    age_max = int(customers_df["age"].max())
    age_range = st.slider(
        "Вікова група",
        min_value=age_min,
        max_value=age_max,
        value=(age_min, age_max),
        help="Виберіть діапазон віку",
    )

    status_filters = st.multiselect(
        "Статус клієнтів",
        options=["Нові", "Постійні", "VIP"],
        help="Виберіть один або декілька статусів. Клієнт може мати декілька статусів одночасно",
    )

    vip_threshold = st.number_input(
        "Поріг VIP (сума витрат, грн)",
        min_value=1000,
        value=10000,
        step=1000,
        help="Клієнти з сумою витрат вище цього порогу вважаються VIP",
    )

    inactive_days = st.number_input(
        "Період неактивності (днів)",
        min_value=30,
        value=60,
        step=30,
        help="Клієнти без покупок протягом цього періоду вважаються неактивними",
    )

mask = (customers_df["store"].isin(selected_stores)) & (
    customers_df["age"].between(age_range[0], age_range[1])
)

if selected_gender != "Всі":
    mask &= customers_df["gender"] == selected_gender

filtered_df = customers_df[mask].copy()

# Add status flags instead of a single segment
filtered_df["is_new"] = filtered_df["total_orders"] == 1
filtered_df["is_regular"] = filtered_df["total_orders"] > 1
filtered_df["is_vip"] = filtered_df["total_spent"] >= vip_threshold

# Apply status filters
if status_filters:
    status_mask = pd.Series(False, index=filtered_df.index)
    if "Нові" in status_filters:
        status_mask |= filtered_df["is_new"]
    if "Постійні" in status_filters:
        status_mask |= filtered_df["is_regular"]
    if "VIP" in status_filters:
        status_mask |= filtered_df["is_vip"]
    filtered_df = filtered_df[status_mask]

# Create a combined status label for display
filtered_df["statuses"] = filtered_df.apply(
    lambda row: " + ".join(
        ["VIP" if row["is_vip"] else "", "Постійний" if row["is_regular"] else "Новий"]
    ).strip(" + "),
    axis=1,
)

st.subheader("📊 Ключові метрики")
kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

total_customers = len(filtered_df)
with kpi1:
    st.metric("Кількість клієнтів", f"{total_customers:,}")

with kpi2:
    avg_orders = filtered_df["total_orders"].mean()
    st.metric("Середня к-сть покупок", f"{avg_orders:.1f}")

with kpi3:
    avg_check = (filtered_df["total_spent"] / filtered_df["total_orders"]).mean()
    st.metric("Середній чек", f"{avg_check:,.2f} ₴")

with kpi4:
    loyal_customers = (filtered_df["total_orders"] > 1).sum()
    loyal_percent = (loyal_customers / total_customers) * 100
    st.metric("Постійні клієнти", f"{loyal_percent:.1f}%")

with kpi5:
    vip_customers = (filtered_df["total_spent"] >= vip_threshold).sum()
    vip_percent = (vip_customers / total_customers) * 100
    st.metric("VIP-клієнти", f"{vip_percent:.1f}%")

tab_names = [
    "🎯 Сегментація",
    "📊 Частота покупок",
    "💰 LTV",
    "👥 Демографія",
    "📈 Динаміка",
    "🔍 Детальна таблиця",
]
tabs = st.tabs(tab_names)

with tabs[0]:  # Segmentation
    st.subheader("🎯 Сегментація клієнтів")
    col1, col2 = st.columns(2)

    with col1:
        # Calculate status combinations
        status_combinations = filtered_df["statuses"].value_counts()
        fig1 = px.pie(
            values=status_combinations.values,
            names=status_combinations.index,
            title="Розподіл клієнтів за статусами",
        )
        st.plotly_chart(fig1, use_container_width=True)

        # Show key stats
        st.markdown("#### Статистика по статусах:")
        st.markdown(
            f"🆕 Нових клієнтів: {filtered_df['is_new'].sum():,} ({filtered_df['is_new'].mean()*100:.1f}%)"
        )
        st.markdown(
            f"🔄 Постійних клієнтів: {filtered_df['is_regular'].sum():,} ({filtered_df['is_regular'].mean()*100:.1f}%)"
        )
        st.markdown(
            f"👑 VIP клієнтів: {filtered_df['is_vip'].sum():,} ({filtered_df['is_vip'].mean()*100:.1f}%)"
        )

    with col2:
        store_dist = filtered_df["store"].value_counts()
        fig2 = px.bar(
            x=store_dist.index,
            y=store_dist.values,
            title="Розподіл клієнтів за магазинами",
            labels={"x": "Магазин", "y": "Кількість клієнтів"},
        )
        st.plotly_chart(fig2, use_container_width=True)

with tabs[1]:  # Frequency
    st.subheader("📊 Аналіз частоти покупок")

    fig3 = px.histogram(
        filtered_df,
        x="total_orders",
        title="Розподіл кількості замовлень",
        labels={"total_orders": "Кількість замовлень", "count": "К-сть клієнтів"},
    )
    st.plotly_chart(fig3, use_container_width=True)

    orders_stats = filtered_df["total_orders"].describe()
    cols = st.columns(3)
    cols[0].metric("Медіанна к-сть замовлень", f"{orders_stats['50%']:.1f}")
    cols[1].metric("Максимальна к-сть замовлень", f"{orders_stats['max']:.0f}")
    freq_pct = (filtered_df["total_orders"] <= 2).mean() * 100
    cols[2].markdown(f"**Інсайт:** {freq_pct:.1f}% клієнтів зробили 1-2 замовлення")

with tabs[2]:  # LTV
    st.subheader("💰 Аналіз Lifetime Value")
    col1, col2 = st.columns(2)

    with col1:
        # Create status comparison
        status_comparison = pd.DataFrame(
            {"Статус": filtered_df["statuses"], "Витрати": filtered_df["total_spent"]}
        )

        fig4 = px.box(
            status_comparison,
            x="Статус",
            y="Витрати",
            title="Розподіл витрат за статусами клієнтів",
            labels={"Витрати": "Сума витрат, грн"},
        )
        st.plotly_chart(fig4, use_container_width=True)

    with col2:
        avg_ltv = filtered_df.groupby("store")["total_spent"].mean()
        fig5 = px.bar(
            x=avg_ltv.index,
            y=avg_ltv.values,
            title="Середній LTV за магазинами",
            labels={"x": "Магазин", "y": "Сума витрат, грн"},
        )
        st.plotly_chart(fig5, use_container_width=True)

with tabs[3]:  # Demographics
    st.subheader("👥 Демографічний аналіз")
    col1, col2 = st.columns(2)

    with col1:
        fig6 = px.histogram(
            filtered_df,
            x="age",
            title="Віковий розподіл клієнтів",
            labels={"age": "Вік", "count": "К-сть клієнтів"},
        )
        st.plotly_chart(fig6, use_container_width=True)

    with col2:
        gender_stats = (
            filtered_df.groupby("gender")
            .agg({"customer_id": "count", "total_spent": "mean"})
            .reset_index()
        )

        fig7 = px.bar(
            gender_stats,
            x="gender",
            y="customer_id",
            title="Розподіл за статтю",
            text=gender_stats["total_spent"].round(2).astype(str) + " ₴",
            labels={"gender": "Стать", "customer_id": "К-сть клієнтів"},
        )
        st.plotly_chart(fig7, use_container_width=True)

with tabs[4]:  # Dynamics
    st.subheader("📈 Динаміка клієнтської бази")

    monthly_signups = pd.DataFrame(
        {
            "month": pd.to_datetime(filtered_df["signup_date"]).dt.to_period("M"),
            "count": 1,
        }
    )
    monthly_signups = monthly_signups.groupby("month")["count"].sum()

    fig8 = px.line(
        x=monthly_signups.index.astype(str),
        y=monthly_signups.values,
        title="Нові клієнти по місяцях",
        labels={"x": "Місяць", "y": "К-сть нових клієнтів"},
    )
    st.plotly_chart(fig8, use_container_width=True)

    inactive_threshold = datetime.now() - timedelta(days=inactive_days)
    inactive_mask = filtered_df["last_purchase_date"] < inactive_threshold
    inactive_count = inactive_mask.sum()
    inactive_pct = (inactive_count / total_customers) * 100

    st.metric(
        "Неактивні клієнти",
        f"{inactive_count} ({inactive_pct:.1f}%)",
        help=f"Клієнти без покупок останні {inactive_days} днів",
    )

with tabs[5]:  # Table
    st.subheader("📋 Детальна інформація про клієнтів")

    display_cols = [
        "customer_id",
        "total_orders",
        "total_spent",
        "last_purchase_date",
        "statuses",
    ]
    table_df = filtered_df[display_cols].copy()
    table_df["avg_check"] = table_df["total_spent"] / table_df["total_orders"]

    st.dataframe(
        table_df,
        column_config={
            "customer_id": "ID клієнта",
            "total_orders": "К-сть замовлень",
            "total_spent": st.column_config.NumberColumn(
                "Сума витрат", format="%.2f ₴"
            ),
            "avg_check": st.column_config.NumberColumn("Середній чек", format="%.2f ₴"),
            "last_purchase_date": st.column_config.DatetimeColumn(
                "Остання покупка", format="DD.MM.YYYY"
            ),
            "statuses": "Статуси клієнта",
        },
        height=400,
    )

    csv = table_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "📥 Експортувати",
        csv,
        "customers_analysis.csv",
        "text/csv",
        help="Завантажити таблицю в форматі CSV",
    )
