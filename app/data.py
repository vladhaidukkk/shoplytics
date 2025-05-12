from dataclasses import dataclass

import pandas as pd
import streamlit as st

st.session_state


@dataclass
class Data:
    key: str
    columns: list[str]

    @property
    def session_state(self) -> pd.DataFrame:
        return st.session_state[self.key]

    @session_state.setter
    def session_state(self, value: pd.DataFrame) -> None:
        st.session_state[self.key] = value


sales_data = Data(
    key="sales_data",
    columns=["date", "product_id", "quantity", "price"],
)

inventory_data = Data(
    key="inventory_data",
    columns=["product_id", "quantity", "last_updated"],
)

customers_data = Data(
    key="customers_data",
    columns=["customer_id", "name"],
)
