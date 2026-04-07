# -*- coding: utf-8 -*-

import sys
import os

BASE_DIR = os.path.dirname(__file__)
SRC_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "src"))
sys.path.insert(0, SRC_DIR)

from models import Product


##############
# TEST CASES #
##############

def test_product_creation():
    dummy = Product("1", "spicy_pickles", "Gurke, würzig", "Single unit of spicy pickles", True)
    assert dummy.product_id == "1"
    assert dummy.product_key == "spicy_pickles"
    assert dummy.product_display_name == "Gurke, würzig"
    assert dummy.product_description == "Single unit of spicy pickles"
    assert dummy.product_is_active


# TODO: add further tests for repr and str
def test_product_repr():
    dummy = Product(product_id="2", product_key="classic_pickles", product_is_active=True)
    assert repr(dummy) == "Product('2', 'classic_pickles', True)"


def test_product_str():
    dummy = Product(product_id="3", product_key="fusion_pickles")
    expected = (
            "Product Details: \n"
            f"{'--'* 14} \n"
            f"Id:           3\n"
            f"Key:          fusion_pickles\n"
            f"Display name: None\n"
            f"Description:  None\n"
            f"Is active:    False\n"
    )
    assert str(dummy) == expected

