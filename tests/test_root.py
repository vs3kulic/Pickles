# -*- coding: utf-8 -*-

"""
API root endpoint tests for the Pickles FastAPI application.

These tests verify that the root (/) endpoint returns a 200 OK status 
    and responds with HTML content.
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

def test_root_returns_ok():
    response = client.get("/")
    assert response.status_code == 200

def test_root_returns_text_html():
    response = client.get("/")
    expected_type = "text/html"
    assert expected_type in response.headers["content-type"]
