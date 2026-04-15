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

    def __init__(
        self,
        quantities: dict | None = None,
    ):
        self._quantities = quantities if quantities is not None else {}

    def add_stock(self, product_id: int, amount: int) -> None:
        self._quantities[product_id] = self._quantities.get(product_id, 0) + amount

    def get_stock(self, product_id: int) -> int:
        return self._quantities.get(product_id, 0)

    def reduce_stock(self, product_id: int, amount: int = 1) -> None:
        if product_id not in self._quantities:
            raise KeyError(f"Product {product_id} not found in inventory.")
        if self._quantities[product_id] < amount:
            raise ValueError(f"Not enough stock for product {product_id}.")
        self._quantities[product_id] -= amount

    def list_inventory(self):
        # Returns a list of (product_id, quantity) tuples
        return list(self._quantities.items())

    def __repr__(self):
        return f"Inventory(quantities={self._quantities})"


# =======================
# Task 4: Order Manager
# =======================

class OrderManager:
    pass


def main():
    # Start with empty inventory
    inv = Inventory()
    print("Initial inventory:", inv.list_inventory())

    # Add stock for both products
    inv.add_stock(product_id=1, amount=10)
    inv.add_stock(2, 5)
    print("After adding stock:", inv.list_inventory())

    # Reduce stock for product 1
    inv.reduce_stock(1, 3)
    print("After reducing 3 from product 1:", inv.list_inventory())

    # Get stock for product 2
    print(f"Stock for product 2: {inv.get_stock(2)}")

if __name__ == "__main__":
    main()
