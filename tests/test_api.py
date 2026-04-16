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

from app import app

client = TestClient(app)

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
def test_reduce_stock():
	# First, ensure there is stock to reduce
	client.post(
		"/api/inventory/add",
		data={"product_id": 102, "product_key": "test_key", "quantity": 3}
	)
	response = client.post(
		"/api/inventory/reduce",
		data={"product_id": 102, "quantity": 2}
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
