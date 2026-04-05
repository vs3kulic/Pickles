# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
import sys, os

#############
# APP SETUP #
#############

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from app import app

client = TestClient(app)

##############
# TEST CASES #
##############

def test_health_returns_ok():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "The Pickles API is available."}
