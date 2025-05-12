from abc import ABC, abstractmethod

import pandas as pd

from app.data import customers_data, inventory_data, sales_data


class DataValidator(ABC):
    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    @abstractmethod
    def validate(self) -> list[str]:
        pass

    def find_missing_columns(self, columns: list[str]) -> list[str]:
        return [col for col in columns if col not in self.df.columns]

    def find_columns_with_missing_values(self) -> list[str]:
        return [col for col in self.df.columns if self.df[col].isnull().any()]


class SalesDataValidator(DataValidator):
    def validate(self) -> list[str]:
        errors = []

        missing_columns = self.find_missing_columns(sales_data.columns)
        if missing_columns:
            errors.append(f"Відсутні обов'язкові колонки: {', '.join(missing_columns)}")

        for col in self.find_columns_with_missing_values():
            errors.append(f"Знайдено пропущені значення в колонці '{col}'")

        if not errors:
            try:
                self.df["date"] = pd.to_datetime(self.df["date"])
            except ValueError:
                errors.append("Колонка 'date' має неправильний формат дати")

        return errors


class InventoryDataValidator(DataValidator):
    def validate(self) -> list[str]:
        errors = []

        missing_columns = self.find_missing_columns(inventory_data.columns)
        if missing_columns:
            errors.append(f"Відсутні обов'язкові колонки: {', '.join(missing_columns)}")

        for col in self.find_columns_with_missing_values():
            errors.append(f"Знайдено пропущені значення в колонці '{col}'")

        if not errors:
            try:
                self.df["last_updated"] = pd.to_datetime(self.df["last_updated"])
            except ValueError:
                errors.append("Колонка 'last_updated' має неправильний формат дати")

        return errors


class CustomersDataValidator(DataValidator):
    def validate(self) -> list[str]:
        errors = []

        missing_columns = self.find_missing_columns(customers_data.columns)
        if missing_columns:
            errors.append(f"Відсутні обов'язкові колонки: {', '.join(missing_columns)}")

        for col in self.find_columns_with_missing_values():
            errors.append(f"Знайдено пропущені значення в колонці '{col}'")

        return errors
