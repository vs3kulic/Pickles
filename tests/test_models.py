# -*- coding: utf-8 -*-

"""
Unit tests for the Product model.

- product_id, product_key: mandatory fields
- product_display_name, product_description: optional fields (default: None)
- product_is_active: boolean, defaults to False

These tests cover object creation, string representations, property access, and property setters.
"""

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
    assert dummy.product_id == "1"                                      # Mandatory attribute
    assert dummy.product_key == "spicy_pickles"                         # Mandatory attribute
    assert dummy.product_display_name == "Gurke, würzig"                # Optional attribute
    assert dummy.product_description == "Single unit of spicy pickles"  # Optional attribute
    assert dummy.product_is_active                                      # default=False


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


def test_product_id_getter():
    dummy = Product(product_id="3", product_key="fusion_pickles")
    assert dummy.product_id == "3"


def test_product_key_getter():
    dummy = Product(product_id="3", product_key="fusion_pickles")
    assert dummy.product_key == "fusion_pickles"


def test_product_display_name_getter():
    dummy = Product("3", "spicy_pickles", "Gurke, exotisch", "Single unit of fusion pickles", True)
    assert dummy.product_display_name == "Gurke, exotisch"


def test_product_description_getter():
    dummy = Product("3", "spicy_pickles", "Gurke, exotisch", "Single unit of fusion pickles", True)
    assert dummy.product_description == "Single unit of fusion pickles"


def test_product_is_active_getter():
    dummy = Product(product_id="3", product_key="fusion_pickles")
    assert not dummy.product_is_active


def test_product_is_active_setter():
    dummy = Product(product_id="3", product_key="fusion_pickles")
    dummy.product_is_active = True
    assert dummy.product_is_active
