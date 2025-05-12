import numpy as np
import pandas as pd

from app.data import customers_data, inventory_data, sales_data


def generate_sample_sales() -> pd.DataFrame:
    dates = pd.date_range(start="2024-01-01", end="2024-12-31", freq="D")
    stores = ["Store A", "Store B", "Store C"]
    categories = ["Футболки", "Штани", "Сукні", "Куртки"]
    sizes = ["XS", "S", "M", "L", "XL"]
    genders = ["Чоловічий", "Жіночий", "Унісекс"]
    age_groups = ["0-2", "3-6", "7-14", "14+"]

    data = []

    for date in dates:
        for _ in range(np.random.randint(5, 15)):  # Random number of sales per day
            store = np.random.choice(stores)
            product_id = f"P{np.random.randint(1, 1001):04d}"
            category = np.random.choice(categories)
            product_name = f"{category} {np.random.randint(1, 100)}"
            size = np.random.choice(sizes)
            gender = np.random.choice(genders)
            age_group = np.random.choice(age_groups)

            quantity = np.random.randint(1, 10)
            price = np.random.uniform(200.0, 2000.0)
            cost = price * 0.6  # 40% margin
            revenue = quantity * price

            data.append(
                [
                    date,
                    store,
                    product_id,
                    product_name,
                    category,
                    size,
                    gender,
                    age_group,
                    quantity,
                    price,
                    cost,
                    revenue,
                ]
            )

    return pd.DataFrame(data, columns=sales_data.column_names)


def generate_sample_inventory() -> pd.DataFrame:
    stores = ["Store A", "Store B", "Store C"]
    categories = ["Футболки", "Штани", "Сукні", "Куртки"]
    sizes = ["XS", "S", "M", "L", "XL"]

    data = []

    for store in stores:
        for category in categories:
            for size in sizes:
                product_id = f"P{np.random.randint(1, 1001):04d}"
                product_name = f"{category} {np.random.randint(1, 100)}"
                stock_qty = np.random.randint(10, 200)
                min_qty = np.random.randint(5, 20)
                last_updated = pd.Timestamp("2024-12-31")

                data.append(
                    [
                        store,
                        product_id,
                        product_name,
                        category,
                        size,
                        stock_qty,
                        min_qty,
                        last_updated,
                    ]
                )

    return pd.DataFrame(data, columns=inventory_data.column_names)


def generate_sample_customers() -> pd.DataFrame:
    stores = ["Store A", "Store B", "Store C"]
    genders = ["Чоловічий", "Жіночий"]

    data = []

    for i in range(1, 101):  # Generate 100 customers
        customer_id = f"C{i:04d}"
        age = np.random.randint(18, 70)
        gender = np.random.choice(genders)
        start_date = pd.Timestamp("2024-01-01")
        days_offset = np.random.randint(0, 365)
        signup_date = start_date + pd.Timedelta(days=days_offset)
        store = np.random.choice(stores)
        total_orders = np.random.randint(1, 20)
        total_spent = np.random.uniform(1000.0, 50000.0)
        last_purchase_date = signup_date + pd.Timedelta(days=np.random.randint(0, 365))

        data.append(
            [
                customer_id,
                age,
                gender,
                signup_date,
                store,
                total_orders,
                total_spent,
                last_purchase_date,
            ]
        )

    return pd.DataFrame(data, columns=customers_data.column_names)
