# -*- coding: utf-8 -*-

import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from models import Product

def test_product_creation():
    dummy = Product("1", "spicy_pickles", "Gurke, würzig", "Single unit of spicy pickles", True)
    assert dummy.product_id == "1"
    assert dummy.product_name == "spicy_pickles"
    assert dummy.product_display_name == "Gurke, würzig"
    assert dummy.product_description == "Single unit of spicy pickles"
    assert dummy.product_is_active

# TODO: add further tests for repr and str
