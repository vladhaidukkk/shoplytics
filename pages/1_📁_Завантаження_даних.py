import io

import pandas as pd
import streamlit as st

from app.data import customers_data, inventory_data, sales_data
from app.data_generators import (
    generate_sample_customers,
    generate_sample_inventory,
    generate_sample_sales,
)
from app.data_validator import DataValidator
from app.pages import dashboard_page, upload_page

upload_page.render()


# Data upload section.
def read_file_content(uploaded_file: io.BytesIO) -> pd.DataFrame:
    if uploaded_file.name.endswith(".csv"):
        return pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith(".xlsx"):
        return pd.read_excel(uploaded_file)
    else:
        raise ValueError("Непідтримуваний формат файлу")


required_files_col, optional_files_col = st.columns(2)

with required_files_col:
    st.subheader("📂 Обов'язкові файли")

    sales_file = st.file_uploader(
        "Завантажте файл продажів (CSV або Excel)",
        type=["csv", "xlsx"],
        help=f"Файл повинен містити колонки: {', '.join(sales_data.column_names)}",
    )
    if sales_file is not None:
        try:
            sales_df = read_file_content(sales_file)
            errors = DataValidator(sales_df, sales_data).validate()

            if not errors:
                sales_data.session_state = sales_df
                st.success("Файл продажів успішно завантажено!", icon="✅")
                st.dataframe(sales_df.head(10), use_container_width=True)
            else:
                st.error(
                    "Помилки у файлі продажів:\n"
                    + "\n".join(f"- {error}" for error in errors),
                    icon="❌",
                )
        except Exception as err:
            st.error(f"Помилка при читанні файлу: {err}", icon="❌")

    inventory_file = st.file_uploader(
        "Завантажте файл складських запасів (CSV або Excel)",
        type=["csv", "xlsx"],
        help=f"Файл повинен містити колонки: {', '.join(inventory_data.column_names)}",
    )
    if inventory_file is not None:
        try:
            inventory_df = read_file_content(inventory_file)
            errors = DataValidator(inventory_df, inventory_data).validate()

            if not errors:
                inventory_data.session_state = inventory_df
                st.success("Файл складських запасів успішно завантажено!", icon="✅")
                st.dataframe(inventory_df.head(10), use_container_width=True)
            else:
                st.error(
                    "Помилки у файлі складських запасів:\n"
                    + "\n".join(f"- {error}" for error in errors),
                    icon="❌",
                )
        except Exception as err:
            st.error(f"Помилка при читанні файлу: {err}", icon="❌")

with optional_files_col:
    st.subheader("Опціональні файли")

    customers_file = st.file_uploader(
        "Завантажте файл клієнтів (CSV або Excel)",
        type=["csv", "xlsx"],
        help=f"Файл повинен містити колонки: {', '.join(customers_data.column_names)}",
    )
    if customers_file is not None:
        try:
            customers_df = read_file_content(customers_file)
            errors = DataValidator(customers_df, customers_data).validate()

            if not errors:
                customers_data.session_state = customers_df
                st.success("Файл клієнтів успішно завантажено!", icon="✅")
                st.dataframe(customers_df.head(10), use_container_width=True)
            else:
                st.error(
                    "Помилки у файлі клієнтів:\n\n"
                    + "\n".join(f"- {error}" for error in errors),
                    icon="❌",
                )
        except Exception as err:
            st.error(f"Помилка при читанні файлу: {err}", icon="❌")

# Sample data download section.
st.divider()
st.subheader("Завантажити приклади файлів")

sample_sales_col, sample_inventory_col, sample_customers_col = st.columns(3)

with sample_sales_col:
    sample_sales = generate_sample_sales().to_csv(index=False).encode("utf-8")
    st.download_button(
        "🛒 Приклад файлу продажів",
        sample_sales,
        "sample_sales.csv",
        "text/csv",
        help="Завантажити приклад файлу з даними про продажі",
    )

with sample_inventory_col:
    sample_inventory = generate_sample_inventory().to_csv(index=False).encode("utf-8")
    st.download_button(
        "📦 Приклад файлу складу",
        sample_inventory,
        "sample_inventory.csv",
        "text/csv",
        help="Завантажити приклад файлу зі складськими даними",
    )

with sample_customers_col:
    sample_customers = generate_sample_customers().to_csv(index=False).encode("utf-8")
    st.download_button(
        "👥 Приклад файлу клієнтів",
        sample_customers,
        "sample_customers.csv",
        "text/csv",
        help="Завантажити приклад файлу з даними про клієнтів",
    )

# Further actions section.
st.divider()

required_data_loaded = (
    sales_data.key in st.session_state and inventory_data.key in st.session_state
)
if required_data_loaded:
    st.success(
        "Всі обов'язкові файли завантажено! Можете перейти до аналітики.", icon="✅"
    )
    st.link_button(
        "➡️ Перейти до аналітики",
        dashboard_page.url,
        use_container_width=True,
        type="primary",
    )
else:
    st.warning(
        (
            "Завантажте обов'язкові файли (продажі та складські запаси) для переходу "
            "до аналітики."
        ),
        icon="⚠️",
    )
