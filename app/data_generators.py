import numpy as np
import pandas as pd

from app.data import customers_data, inventory_data, sales_data


def generate_sample_sales() -> pd.DataFrame:
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    products = range(1, 11)
    data = []

    for date in dates:
        for product in products:
            quantity = np.random.randint(1, 100)
            price = np.random.uniform(10.0, 1000.0)
            data.append([date, product, quantity, round(price, 2)])

    return pd.DataFrame(data, columns=sales_data.columns)


def generate_sample_inventory() -> pd.DataFrame:
    products = range(1, 21)
    data = []

    for product in products:
        quantity = np.random.randint(50, 1000)
        last_updated = pd.Timestamp("2024-12-31")
        data.append([product, quantity, last_updated])

    return pd.DataFrame(data, columns=inventory_data.columns)


def generate_sample_customers() -> pd.DataFrame:
    customer_ids = range(1, 51)
    names = [f"Customer {i}" for i in customer_ids]
    data = list(zip(customer_ids, names))

    return pd.DataFrame(data, columns=customers_data.columns)
