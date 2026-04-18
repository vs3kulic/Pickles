# -*- coding: utf-8 -*-
from src.repository import GoogleSheetsRepository as gsr

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

    def __repr__(self):
        return f"Inventory(quantities={self._quantities})"

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

    @classmethod
    def from_repo(cls, entity: str = "inventory"):
        """Load inventory quantities from repository and return Inventory instance and repo."""
        repo = gsr.get_repo(entity=entity)
        inventory_data = repo.load()
        quantities = {
            int(row["product_id"]): int(row["product_quantity"])
            for row in inventory_data
        }
        return cls(quantities), repo

    def apply_quantity_change(
        self,
        product_id: int,
        product_key: str,
        change: int,
        action: str,
        repo=None
    ) -> dict:
        """Add or reduce stock and update repo accordingly."""
        if repo is None:
            # fallback: load repo if not provided
            _, repo = self.from_repo()
        current_quantity = self.get_stock(product_id)

        if action == "add":
            if current_quantity != 0:
                new_quantity = current_quantity + change
                repo.update_quantity(product_id, new_quantity)
                self._quantities[product_id] = new_quantity
                return {"status": "success", "new_quantity": new_quantity}
            else:
                repo.save({
                    "product_id": product_id,
                    "product_key": product_key,
                    "product_quantity": change
                })
                self._quantities[product_id] = change
                return {"status": "success", "new_quantity": change}

        if action == "reduce":
            if current_quantity == 0:
                return {
                    "status": "error",
                    "message": f"Product ID {product_id} not found in inventory."
                }
            if current_quantity < change:
                return {
                    "status": "error",
                    "message": f"Not enough stock for product {product_id}."
                }
            new_quantity = current_quantity - change
            repo.update_quantity(product_id, new_quantity)
            self._quantities[product_id] = new_quantity
            return {"status": "success", "new_quantity": new_quantity}

        return {"status": "error", "message": "Invalid action."}
