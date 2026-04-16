# -*- coding: utf-8 -*-


"""
API tests for the Pickles FastAPI app.

These tests use FastAPI's TestClient to test the /api/inventory/add and /api/inventory/reduce endpoints.
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from src.app import app

client = TestClient(app)

import random

@pytest.fixture
def unique_product_id():
	"""Fixture that returns a unique random product ID as an int."""
	return random.randint(10000, 99999)

# Example API test for add_to_stock
def test_add_to_stock():
	response = client.post(
		"/api/inventory/add",
		data={"product_id": 101, "product_key": "test_key", "quantity": 5}
	)
	assert response.status_code == 200
	assert response.json()["status"] == "success"
	assert "new_quantity" in response.json()

# Example API test for reduce_stock
def test_reduce_stock(unique_product_id):
	pid = unique_product_id
	client.post(
		"/api/inventory/add",
		data={"product_id": pid, "product_key": "test_key", "quantity": 3}
	)
	response = client.post(
		"/api/inventory/reduce",
		data={"product_id": pid, "quantity": 2}
	)
	assert response.status_code == 200
	assert response.json()["status"] == "success"
	assert response.json()["new_quantity"] == 1

# Example: test reduce too much
def test_reduce_too_much():
	client.post(
		"/api/inventory/add",
		data={"product_id": 103, "product_key": "test_key", "quantity": 1}
	)
	response = client.post(
		"/api/inventory/reduce",
		data={"product_id": 103, "quantity": 5}
	)
	assert response.status_code == 200
	assert response.json()["status"] == "error"
	assert "Not enough stock" in response.json()["message"]
