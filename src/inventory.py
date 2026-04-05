# -*- coding: utf-8 -*-

# =======================
# Task 3: Inventory Class
# =======================
# Write an Inventory class that helps you manage products and orders:
# - products: a dictionary mapping product_id to Product
# - orders: a list of Order objects
# [ ] Set up __init__ to initialize products and orders
# [ ] add_product(product: Product) to add a product to the inventory
# [ ] remove_product(product_id: str) to remove a product by its ID
# [ ] get_product(product_id: str) to fetch a product (or return None if not found)
# [ ] list_products() to return all products as a list
# [ ] add_order(order: Order) to add a new order
# [ ] list_orders() to return all orders as a list
# [ ] (Optional) Save or load the inventory to/from a file (serialization)
# [ ] Use getters and setters for products and orders if you want more control
# [ ] Static method: validate_inventory_data(data: dict) to check if inventory data is valid
# [ ] Class method: from_dict(data: dict) to create an Inventory from a dictionary
# [ ] (Optional) Use an abstract base class if you want to share methods across models

