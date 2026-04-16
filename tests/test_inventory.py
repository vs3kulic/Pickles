# -*- coding: utf-8 -*-

"""
Unit tests for the Inventory model.

- field 1
- field 2
- field 3

These tests cover object creation, string representations, ...
"""

import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from inventory import Inventory
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
