# -*- coding: utf-8 -*-

"""
Unit tests for the GoogleSheetsRepository models.
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from models import Product
from repository import GoogleSheetsConnector, GoogleSheetsRepository


############
# FIXTURES #
############

@pytest.fixture
def mock_connector():
    connector = MagicMock()
    worksheet = MagicMock()
    connector.get_worksheet.return_value = worksheet
    return connector, worksheet

@pytest.fixture
def max_dummy():
    return Product(
        3,
        "spicy_pickles",
        "Gurke, exotisch", 
        "Single unit of fusion pickles", 
        True
    )

##############
# TEST CASES #
##############

def test_load_returns_records(mock_connector: MagicMock, max_dummy):
    connector, worksheet = mock_connector
    worksheet.get_all_records.return_value = [max_dummy]

    repo = GoogleSheetsRepository(connector, "products")
    result = repo.load()

    assert result == [max_dummy]


def test_save_appends_row(mock_connector: MagicMock):
    connector, worksheet = mock_connector
    worksheet.row_values.return_value = ["product_id", "product_key"]

    repo = GoogleSheetsRepository(connector, "products")
    repo.save({"product_id": 5, "product_key": "fusion_pickles"})

    worksheet.append_row.assert_called_once_with([5, "fusion_pickles"])


def test_repository_str(mock_connector: MagicMock):
    connector, _ = mock_connector
    connector.__str__ = MagicMock(
        return_value="GoogleSheetsConnector(document='Pickles DB')"
    )
    entity = "products"
    repo = GoogleSheetsRepository(connector, entity)

    expected = (
        "GoogleSheetsRepository("
        f"connector='{connector}', "
        f"worksheet='{entity}')"
    )
    assert str(repo) == expected
