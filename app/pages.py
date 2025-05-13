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


home_page = Page(
    url="Головна",
    title="Shoplytics",
    icon="✨",
    description="""
        Shoplytics - це потужна аналітична платформа, розроблена спеціально для бізнесу
        електронної комерції. Вона допомагає перетворити ваші дані про продажі, запаси
        та клієнтів у корисні бізнес-інсайти.
    """,
)

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

dashboard_page = Page(
    url="Оглядова_панель",
    title="Оглядова панель",
    icon="📊",
    description="""
        Оглядова панель надає загальний огляд основних показників вашого бізнесу.
    """,
)

sales_page = Page(
    url="Продажі",
    title="Аналіз продажів",
    icon="🛍️",
    description="""
        Аналізуйте дані про продажі, щоб виявити тренди, сезонність та інші
        закономірності. Використовуйте ці дані для оптимізації асортименту,
        планування акцій та підвищення ефективності продажів.
    """,
)

inventory_page = Page(
    url="Складські_запаси",
    title="Аналіз складських запасів",
    icon="📦",
    description="""
        Аналізуйте складські запаси, щоб виявити товари з низьким обігом, уникнути
        дефіциту чи надлишків, та оптимізувати рівень запасів для ефективного
        управління складом.
    """,
)

customers_page = Page(
    url="Клієнти",
    title="Аналіз клієнтів",
    icon="👥",
    description="""
        Аналізуйте базу клієнтів, щоб краще розуміти хто є вашими покупцями, їхню
        поведінку та цінність для бізнесу. Використовуйте ці дані для персоналізації
        пропозицій, утримання постійних клієнтів та залучення нових.
    """,
)
