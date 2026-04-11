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
import pytest

# pylint: disable=redefined-outer-name


############
# FIXTURES #
############

@pytest.fixture
def min_dummy():
    return Product(product_id=3, product_key="fusion_pickles")


@pytest.fixture
def max_dummy():
    return Product(3, "spicy_pickles", "Gurke, exotisch", "Single unit of fusion pickles", True)


##############
# TEST CASES #
##############

def test_product_creation(max_dummy):
    assert max_dummy.product_id == 3                                            # Mandatory attribute
    assert max_dummy.product_key == "spicy_pickles"                             # Mandatory attribute
    assert max_dummy.product_display_name == "Gurke, exotisch"                  # Optional attribute
    assert max_dummy.product_description == "Single unit of fusion pickles"     # Optional attribute
    assert max_dummy.product_is_active                                          # default=False


def test_product_repr(min_dummy):
    assert repr(min_dummy) == "Product(3, 'fusion_pickles', False)"


def test_product_str(min_dummy):
    expected = (
            "Product Details: \n"
            f"{'--'* 14} \n"
            f"Id:           3\n"
            f"Key:          fusion_pickles\n"
            f"Display name: None\n"
            f"Description:  None\n"
            f"Is active:    False\n"
    )
    assert str(min_dummy) == expected


def test_product_id_getter(min_dummy):
    assert min_dummy.product_id == 3


def test_product_key_getter(min_dummy):
    assert min_dummy.product_key == "fusion_pickles"


def test_product_display_name_getter(max_dummy):
    assert max_dummy.product_display_name == "Gurke, exotisch"


def test_product_description_getter(max_dummy):
    assert max_dummy.product_description == "Single unit of fusion pickles"


def test_product_is_active_getter(min_dummy):
    assert not min_dummy.product_is_active


def test_product_is_active_setter(min_dummy):
    min_dummy.product_is_active = True
    assert min_dummy.product_is_active
