# -*- coding: utf-8 -*-

from fastapi.testclient import TestClient
import sys, os
from app import app

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'app'))

client = TestClient(app)

def test_root_returns_ok():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "Welcome to the Pickles API"}
