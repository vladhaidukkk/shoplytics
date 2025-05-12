from dataclasses import dataclass
from typing import Literal, TypeAlias

import pandas as pd
import streamlit as st

ColumnType: TypeAlias = Literal["string", "numeric", "datetime"]
Column: TypeAlias = tuple[str, ColumnType, dict | None]
Columns: TypeAlias = list[Column]


@dataclass
class DataConfig:
    key: str
    columns: Columns

    @property
    def column_names(self) -> list[str]:
        return [col[0] for col in self.columns]

    @property
    def session_state(self) -> pd.DataFrame:
        return st.session_state[self.key]

    @session_state.setter
    def session_state(self, value: pd.DataFrame) -> None:
        st.session_state[self.key] = value


sales_data = DataConfig(
    key="sales_data",
    columns=[
        ("date", "datetime", None),
        ("store", "string", None),
        ("product_id", "string", None),
        ("product_name", "string", None),
        ("category", "string", None),
        ("size", "string", None),
        ("gender", "string", None),
        ("age_group", "string", None),
        ("quantity", "numeric", {"min": 1}),
        ("price", "numeric", {"min": 0}),
        ("cost", "numeric", {"min": 0}),
        ("revenue", "numeric", {"min": 0}),
    ],
)

inventory_data = DataConfig(
    key="inventory_data",
    columns=[
        ("store", "string", None),
        ("product_id", "string", None),
        ("product_name", "string", None),
        ("category", "string", None),
        ("size", "string", None),
        ("stock_qty", "numeric", {"min": 0}),
        ("min_qty", "numeric", {"min": 0}),
        ("last_updated", "datetime", None),
    ],
)

customers_data = DataConfig(
    key="customers_data",
    columns=[
        ("customer_id", "string", None),
        ("age", "numeric", {"min": 0}),
        ("gender", "string", None),
        ("signup_date", "datetime", None),
        ("store", "string", None),
        ("total_orders", "numeric", {"min": 1}),
        ("total_spent", "numeric", {"min": 0}),
        ("last_purchase_date", "datetime", None),
    ],
)
