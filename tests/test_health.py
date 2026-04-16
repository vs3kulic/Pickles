# -*- coding: utf-8 -*-

"""
API health check test for the Pickles FastAPI application.

This test verifies that the /health endpoint returns a 200 OK status 
    and the expected JSON response, confirming the API is available.
"""
# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
import sys, os

#############
# APP SETUP #
#############

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from src.app import app

client = TestClient(app)

##############
# TEST CASES #
##############

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "The Pickles API is available."}
