# -*- coding: utf-8 -*-

import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from models import Product

def test_product_creation():
    dummy = Product("1", "spicy_pickles", "Gurke, würzig", "Single unit of spicy pickles", True)
    # TODO: add @property getters for all fields in Product and update the test to use them
    assert dummy._product_id == "1"
    assert dummy._product_name == "spicy_pickles"
    assert dummy._product_display_name == "Gurke, würzig"
    assert dummy._product_description == "Single unit of spicy pickles"
    assert dummy._product_is_active == True

# TODO: add further tests for repr and str
