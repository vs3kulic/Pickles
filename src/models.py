# -*- coding: utf-8 -*-

# =====================
# Task 1: Product Class
# =====================
# [ ] Implement a Product class with:
#     - Fields: product_id (str), name (str), price (float), stock (int), active (bool)
# [ ] __init__ method to set all fields
# [ ] is_in_stock(quantity: int) -> bool: returns True if stock >= quantity
# [ ] decrease_stock(quantity: int) -> None: subtracts quantity from stock (if enough stock)
# [ ] increase_stock(quantity: int) -> None: adds quantity to stock
# [ ] __repr__ or __str__ for debugging
# [ ] (Optional) to_dict() -> dict for serialization
# [ ] Getters and setters for fields (use @property for price, stock, etc.)
# [ ] Static method: validate_product_data(data: dict) -> bool
# [ ] Class method: from_dict(data: dict) -> Product
# [ ] (Optional) Abstract base class for shared model methods (e.g., to_dict, from_dict)

class Product:
    pass


# ====================
# Task 2: Order Class
# ====================
# [ ] Implement an Order class with:
#     - Fields: order_id (str), customer_name (str), contact (str), product_id (str), quantity (int), timestamp (str), status (str)
# [ ] __init__ method to set all fields
# [ ] to_dict() -> dict: returns a dictionary representation
# [ ] from_dict(data: dict) -> Order: classmethod to create an Order from a dict
# [ ] __repr__ or __str__ for debugging
# [ ] Getters and setters for fields (use @property for status, quantity, etc.)
# [ ] Static method: validate_status(status: str) -> bool
# [ ] Class method: generate_order_id() -> str
# [ ] (Optional) Abstract base class for shared model methods (e.g., to_dict, from_dict)

class Order:
    pass
