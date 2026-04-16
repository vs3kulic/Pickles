# -*- coding: utf-8 -*-

"""
API tests for the inventory management endpoints.

These tests verify the FastAPI inventory API using TestClient and an in-memory 
    mock repository.

Test coverage includes:
- /api/inventory/add: Ensures adding stock updates inventory and returns
    correct status and quantity.
- /api/inventory/reduce: Ensures reducing stock updates inventory and returns
    correct status and quantity.
- /api/inventory/reduce (over-reduce): Ensures reducing more than available
    stock returns an error and does not update inventory.

All tests use monkeypatching to avoid real Google Sheets API calls and ensure fast, isolated test runs.
"""
# tests/test_inventory_api.py
import os
import sys
import random
from unittest.mock import MagicMock

import pytest
from fastapi.testclient import TestClient

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from src.app import app
import src.utils as utils
import src.app as app_module

############
# FIXTURES #
############

@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def unique_product_id():
    return random.randint(10000, 99999)


@pytest.fixture(autouse=True)
def fake_inventory_repo(monkeypatch):
    inventory = {}
    mock_repo = MagicMock()

    def mock_load():
        return [
            {"product_id": pid, "product_quantity": qty}
            for pid, qty in inventory.items()
        ]

    def mock_save(row):
        inventory[int(row["product_id"])] = int(row["product_quantity"])

    def mock_update_quantity(product_id, new_quantity):
        inventory[int(product_id)] = int(new_quantity)

    def mock_get_quantities(entity="inventory"):
        return mock_repo, dict(inventory)

    mock_repo.load.side_effect = mock_load
    mock_repo.save.side_effect = mock_save
    mock_repo.update_quantity.side_effect = mock_update_quantity

    monkeypatch.setattr(utils, "get_quantities", mock_get_quantities)

    # If routes imported get_quantities directly, patch there too.
    if hasattr(app_module, "get_quantities"):
        monkeypatch.setattr(app_module, "get_quantities", mock_get_quantities)

    yield inventory, mock_repo


##############
# TEST CASES #
##############

def test_add_to_stock(client):
    response = client.post(
        "/api/inventory/add",
        data={"product_id": 101, "product_key": "test_key", "quantity": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["new_quantity"] == 5


def test_reduce_stock(client, unique_product_id):
    pid = unique_product_id

    add_response = client.post(
        "/api/inventory/add",
        data={"product_id": pid, "product_key": "test_key", "quantity": 3},
    )
    assert add_response.status_code == 200

    response = client.post(
        "/api/inventory/reduce",
        data={"product_id": pid, "quantity": 2},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "success"
    assert body["new_quantity"] == 1


def test_reduce_too_much(client, unique_product_id):
    pid = unique_product_id

    client.post(
        "/api/inventory/add",
        data={"product_id": pid, "product_key": "test_key", "quantity": 1},
    )

    response = client.post(
        "/api/inventory/reduce",
        data={"product_id": pid, "quantity": 5},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["status"] == "error"
    assert "Not enough stock" in body["message"]
