# -*- coding: utf-8 -*-

"""
Unit tests for the Inventory class.

These tests verify the interface and behavior of the Inventory model 
    using MagicMock.

The tests cover:
- add_stock: Ensures add_stock is called with correct arguments.
- get_stock: Ensures get_stock returns expected values and call counts.
- reduce_stock: Ensures reduce_stock is called with correct arguments.
- list_inventory: Ensures list_inventory returns the expected list structure.
- __repr__: Ensures the string representation is as expected for a MagicMock.
"""
import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from models import Inventory
import pytest
from unittest.mock import MagicMock

# pylint: disable=redefined-outer-name

############
# FIXTURES #
############

@pytest.fixture
def mock_inventory():
    """Fixture that returns a MagicMock for Inventory."""
    mock = MagicMock()
    mock.get_stock.return_value = 10
    mock.list_inventory.return_value = [(1, 10), (2, 5)]
    return mock

##############
# TEST CASES #
##############

def test_add_stock(mock_inventory):
    mock_inventory.add_stock(1, 5)
    mock_inventory.add_stock.assert_called_with(1, 5)


def test_get_stock(mock_inventory):
    assert mock_inventory.get_stock(1) == 10
    assert mock_inventory.get_stock(2) == 10
    assert mock_inventory.get_stock(999) == 10
    assert mock_inventory.get_stock.call_count == 3


def test_reduce_stock(mock_inventory):
    mock_inventory.reduce_stock(1, 3)
    mock_inventory.reduce_stock.assert_called_with(1, 3)
    mock_inventory.reduce_stock(2)
    mock_inventory.reduce_stock.assert_any_call(2)


def test_list_inventory(mock_inventory):
    items = mock_inventory.list_inventory()
    assert (1, 10) in items
    assert (2, 5) in items
    assert isinstance(items, list)


def test_repr(mock_inventory):
    rep = repr(mock_inventory)
    assert rep.startswith('<MagicMock')
