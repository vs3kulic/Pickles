# -*- coding: utf-8 -*-
"""This module contains the repository layer for the Pickles API."""

from abc import ABC, abstractmethod
import os
import gspread


class Repository(ABC):

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def save(self, data: dict) -> None:
        """Persist one record."""
        raise NotImplementedError("Subclasses must implement this method.")

    @abstractmethod
    def load(self) -> list[dict]:
        """Return all records."""
        raise NotImplementedError("Subclasses must implement this method.")

    def __str__(self):
        return f"Repository(name={self._name})"


class GoogleSheetsRepository(Repository):

    def __init__(self, document: str, entity: str):
        super().__init__(entity)  # represents entity, stored as self._name
        self._document = document
        gdoc = self._connect()  # call the helper to open the db
        self._worksheet = gdoc.worksheet(self._name)  # returns gspread object

    def _connect(self) -> gspread.Spreadsheet:
        creds_path = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
        gclient = gspread.service_account(filename=creds_path)
        return gclient.open(self._document)

    def load(self) -> list[dict]:
        try:
            return self._worksheet.get_all_records()
        except gspread.exceptions.APIError as e:
            raise RuntimeError(f"Failed to load '{self._name}': {e}") from e

    def save(self, data: dict) -> None:
        """
        Persist one record.
        
        Args:
            data: The record to persist. Keys must match the worksheet
            column headers, in the same order.
        
        Raises:
            TypeError: If data is not a dictionary.
            RuntimeError: If an API error occurs.
        """
        if not isinstance(data, dict):
            raise TypeError(f"'data' must be a dict, got {type(data).__name__}")
        try:
            self._worksheet.append_row(list(data.values()))
        except gspread.exceptions.APIError as e:
            raise RuntimeError(f"Failed to save to '{self._name}': {e}") from e

    def __str__(self) -> str:
        return (f"GoogleSheetsRepository("
                f"document='{self._document}', "
                f"worksheet='{self._name}')"
        )
