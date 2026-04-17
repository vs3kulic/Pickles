# -*- coding: utf-8 -*-
"""This module contains the repository layer for the Pickles API."""

from abc import ABC, abstractmethod
import os
import gspread


class Repository(ABC):

    def __init__(self, name: str):
        self._name = name
    

    @abstractmethod
    def load(self) -> list[dict]:
        """Return all records."""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def save(self, data: dict) -> None:
        """Persist one record."""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def update_quantity(self, product_id: int, new_quantity: int) -> None:
        """Update the quantity for a given product_id."""
        raise NotImplementedError("Subclasses must implement this method.")

    def __str__(self):
        return f"Repository(name={self._name})"


class GoogleSheetsConnector:

    def __init__(self, document: str):
        self._document = document
        gclient = self._authenticate()
        self._gdoc = gclient.open(self._document)

    def _authenticate(self):
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        if not creds_path:
            raise EnvironmentError("GOOGLE_APPLICATION_CREDENTIALS is not set.")
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Credentials file not found: {creds_path}")
        return gspread.service_account(filename=creds_path)

    def get_worksheet(self, name: str) -> gspread.Worksheet:
        try:
            return self._gdoc.worksheet(name)
        except gspread.WorksheetNotFound as e:
            raise ValueError(
                f"Worksheet {name} not found in {self._document}."
            ) from e

    def __str__(self) -> str:
        return f"GoogleSheetsConnector(document='{self._document}')"


class GoogleSheetsRepository(Repository):

    def __init__(self, connector: GoogleSheetsConnector, entity: str):
        super().__init__(entity)
        self._connector = connector
        self._worksheet = connector.get_worksheet(entity)

    def load(self) -> list[dict]:
        return self._worksheet.get_all_records()

    def update_quantity(self, product_id: int, new_quantity: int) -> None:
        """Update the quantity for a given product_id."""
        # Find the row with the given product_id
        records = self._worksheet.get_all_records()
        headers = self._worksheet.row_values(1)
        qty_col = headers.index("product_quantity") + 1
        for idx, record in enumerate(records, start=2):  # Data starts at row 2
            if str(record["product_id"]) == str(product_id):
                # Update the quantity in the correct cell
                self._worksheet.update_cell(idx, qty_col, new_quantity)
                return
        raise ValueError(f"Product ID {product_id} not found in inventory.")

    def save(self, data: dict) -> None:
        """Persist one record."""
        if not isinstance(data, dict):
            raise TypeError(f"'data' must be a dict, got {type(data).__name__}")

        headers = self._worksheet.row_values(1)
        row = [data[header] for header in headers]
        self._worksheet.append_row(row)

    def __str__(self) -> str:
        return ("GoogleSheetsRepository("
                f"connector='{self._connector}', "
                f"worksheet='{self._name}')"
        )
