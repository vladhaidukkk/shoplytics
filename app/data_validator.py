from typing import Callable, TypeAlias

import pandas as pd

from app.data import Column, ColumnType, DataConfig

TypeValidator: TypeAlias = Callable[[str, dict | None], list[str]]


class DataValidator:
    def __init__(self, df: pd.DataFrame, data_config: DataConfig) -> None:
        self.df = df
        self.data_config = data_config

    def validate(self) -> list[str]:
        errors = []

        # Check for missing columns.
        missing_columns = self._find_missing_columns()
        if missing_columns:
            errors.append(f"Відсутні обов'язкові колонки: {', '.join(missing_columns)}")

        # Check for missing values.
        for col in self._find_columns_with_missing_values():
            errors.append(f"Знайдено пропущені значення в колонці '{col}'")

        # If we have missing columns and values, no need to continue validation.
        if errors:
            return errors

        # Validate each column according to its type and rules.
        for column in self.data_config.columns:
            errors.extend(self._validate_column(column))

        return errors

    def _find_missing_columns(self) -> list[str]:
        return [
            col_name
            for col_name in self.data_config.column_names
            if col_name not in self.df.columns
        ]

    def _find_columns_with_missing_values(self) -> list[str]:
        return [col for col in self.df.columns if self.df[col].isnull().any()]

    def _validate_column(self, column: Column) -> list[str]:
        type_to_validator: dict[ColumnType, TypeValidator] = {
            "string": self._validate_string,
            "numeric": self._validate_numeric,
            "datetime": self._validate_datetime,
        }

        col_name, col_type, rules = column
        validator = type_to_validator.get(col_type)
        if not validator:
            return [f"Невідомий тип колонки '{col_type}' для '{col_name}'"]
        return validator(col_name, rules)

    def _validate_string(
        self, column_name: str, rules: dict | None = None
    ) -> list[str]:
        errors = []
        if not self.df[column_name].astype(str).str.strip().notna().all():
            errors.append(f"Колонка '{column_name}' має містити непорожні значення")
        return errors

    def _validate_numeric(
        self, column_name: str, rules: dict | None = None
    ) -> list[str]:
        errors = []
        if not pd.to_numeric(self.df[column_name], errors="coerce").notnull().all():
            errors.append(f"Колонка '{column_name}' має містити числові значення")
        elif rules and "min" in rules:
            min_value = rules["min"]
            if (self.df[column_name] < min_value).any():
                errors.append(
                    f"Колонка '{column_name}' має містити значення >= {min_value}"
                )
        return errors

    def _validate_datetime(
        self, column_name: str, rules: dict | None = None
    ) -> list[str]:
        errors = []
        try:
            self.df[column_name] = pd.to_datetime(self.df[column_name])
        except ValueError:
            errors.append(f"Колонка '{column_name}' має неправильний формат дати")
        return errors
