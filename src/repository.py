# -*- coding: utf-8 -*-
import gspread
import os

# ========================
# Task 5: Repository Layer
# ========================

#
# Task 5a
#
# Create an abstract base class "Repository" that defines a common interface
# for all storage backends. The class should have the following:
#
# [x] "__init__(self, name: str)": Initializes the repository with a name
#   (e.g. "products" or "orders"). Store it as an instance attribute.
#
# [x] "save(self, data: dict) -> None": An abstract method. Subclasses must
#   override this to store the given dict somewhere.
#   Raise a TypeError if "data" is not a dict.
#
# [x] "load(self) -> list[dict]": An abstract method. Subclasses must override
#   this to retrieve and return data from storage.
#
# [x] "__str__(self)": Returns a human-readable string describing the repository,
#   e.g. "Repository(name='products')"
#
# Attempting to create a "Repository" object directly should raise a TypeError.
#
# Tip: use the "abc" module (ABC, abstractmethod).

# Your code here #
from abc import ABC, abstractmethod

class Repository(ABC):

    def __init__(self, name: str):
        self._name = name

    @abstractmethod
    def save(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise TypeError(f"Save method expects a dict, got {type(dict).__name__}")
        raise NotImplementedError

    @abstractmethod
    def load(self) -> list[dict]:
        raise NotImplementedError

    def __str__(self):
        return f"Repository(name={self._name})"


#
# Task 5b
#
# Create a class "GoogleSheetsRepository" derived from "Repository".
# It reads and writes data to a Google Sheet using gspread.
#
# Credentials are loaded securely from the environment variable:
#   GOOGLE_APPLICATION_CREDENTIALS  -- path to the service account JSON key
# Never hardcode credentials or store the key file in the repo.
# Both Google Sheets API and Google Drive API must be enabled in your project.
#
# > "__init__(self, tab_name: str, document: str)":
#   Initializes the repository with a tab name (e.g. "products") and the Google
#   Sheet document name (e.g. "Pickles DB"). Delegates authentication and
#   worksheet setup to the private helper "_connect()".
#
# > "_connect(self) -> None":
#   Private helper called by "__init__". Loads credentials from the environment,
#   authenticates with gspread, opens the document, and stores the worksheet
#   tab as "self._worksheet".
#
# > "save(self, data: dict) -> None": Appends the given dict as a new row to
#   the worksheet. The dict values form the data row.
#   Raise a TypeError if "data" is not a dict.
#   Handle gspread API errors gracefully.
#
# > "load(self) -> list[dict]": Fetches all rows from the worksheet and returns
#   them as a list of dicts (using the first row as headers/keys).
#   Return an empty list if the sheet has no data yet.
#   Handle gspread API errors gracefully.
#
# > "__str__(self)": Returns a string like:
#   "GoogleSheetsRepository(name='products', sheet_name='Pickles DB')"

# Your code here #
class GoogleSheetsRepository(Repository):

    def __init__(self, tab_name: str, document: str):
        super().__init__(tab_name)  # represents what the repository manages (tab -> entity name)
        self._document = document
        self._connect()             # helper method for authentication

    def _connect(self) -> None:
        # TODO: Load credentials from environment variable
        # TODO: Authenticate with Google using the service account credentials
        # TODO: Open the sheet document, then the specific worksheet tab

    def save(self, data: dict) -> None:
        pass

    def load(self) -> list[dict]:
        pass

    def __str__(self) -> str:
        pass

