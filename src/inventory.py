# -*- coding: utf-8 -*-
from models import Product

# =======================
# Task 3: Inventory Class
# =======================
#
# The Inventory class is responsible only for managing products.
# All order-related logic is handled by the OrderManager class (see Task 4)
#     and the Order model (see Task 2 in models.py).
#
# Requirements:
# - products: a dictionary mapping product_id to Product
# - [x] __init__(): initialize products (empty or from provided dict)
# - [x] add_product(product: Product): add a product to the inventory
# - [ ] remove_product(product_id: str): remove a product by its ID
# - [ ] get_product(product_id: str): fetch a product (or return None if not found)
# - [ ] list_products(): return all products as a list
# - [ ] (Optional) Save or load the inventory to/from a file (serialization)
# - [ ] (Optional) Use getters and setters for products if you want more control
# - [ ] @staticmethod validate_inventory_data(data: dict): check if inventory data is valid
# - [ ] @classmethod from_dict(data: dict): create an Inventory from a dictionary
# - [ ] (Optional) Use an abstract base class if you want to share methods across models

class Inventory:

    def __init__(self, products=None):
        self._products = products if products is not None else {}

    def add_product(self, product: Product):
        # Store product in inventory, using product_id as key
        self._products[product.product_id] = product

    # TODO: review method
    def remove_product(self, product_id: str):
        self._products.pop(product_id, None)

    # TODO: review method
    def get_product(self, product_id: str):
        return self._products.get(product_id)

    def list_products(self):
        return list(self._products.values())
    
    def __repr__(self):
        return f"Inventory({self._products})"


# =======================
# Task 4: Order Manager
# =======================

class OrderManager:
    pass


def main():
    # Create some Product objects
    p1 = Product(product_id=1, product_key="pickles")
    p2 = Product(product_id=2, product_key="olives")

    products_dict = {
        p1.product_id: p1,
        p2.product_id: p2
    }

    inv = Inventory(products=products_dict)
    print(repr(inv))

if __name__ == "__main__":
    main()
