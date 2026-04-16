# -*- coding: utf-8 -*-
"""This module contains utils for the Pickles application."""
from src.repository import GoogleSheetsConnector, GoogleSheetsRepository

def get_product_repo():
    connector = GoogleSheetsConnector("Pickles DB")
    repo = GoogleSheetsRepository(connector, "products")
    return repo


def get_inventory_repo_and_quantities():
    connector = GoogleSheetsConnector("Pickles DB")
    repo = GoogleSheetsRepository(connector, "inventory")
    inventory_data = repo.load()
    quantities = {
        int(row["product_id"]): int(row["product_quantity"])
        for row in inventory_data
    }
    return repo, quantities


def apply_quantity_change(
    product_id: int,
    product_key: str,
    change: int,
    action: str
) -> dict:
    repo, quantities = get_inventory_repo_and_quantities()
    current_quantity = quantities.get(product_id)

    if action == "add":
        if current_quantity is not None:
            new_quantity = current_quantity + change
            repo.update_quantity(product_id, new_quantity)
            return {"status": "success", "new_quantity": new_quantity}
        else:
            repo.save({
                "product_id": product_id,
                "product_key": product_key,
                "product_quantity": change
            })
            return {"status": "success", "new_quantity": change}

    if action == "reduce":
        if current_quantity is None:
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
        return {"status": "success", "new_quantity": new_quantity}

    return {"status": "error", "message": "Invalid action."}
