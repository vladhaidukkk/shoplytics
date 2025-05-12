from dataclasses import dataclass

import streamlit as st
from streamlit.commands.page_config import Layout


@dataclass
class Page:
    url: str
    title: str
    icon: str
    description: str | None = None
    layout: Layout = "wide"

    def render(self) -> None:
        st.set_page_config(
            page_title=f"{self.title} | Shoplytics",
            page_icon=self.icon,
            layout=self.layout,
        )
        st.title(f"{self.icon} {self.title}")
        st.markdown(self.description)


upload_page = Page(
    url="Завантаження_даних",
    title="Завантаження даних",
    icon="📁",
    description="""
        Завантажте необхідні файли для аналізу. Файли продажів та складських запасів
        є обов'язковими для роботи системи. Дані буде збережено в рамках поточної
        сесії.
    """,
)

dashboard_page = Page(url="Оглядова_панель", title="Оглядова панель", icon="📊")
