# -*- coding: utf-8 -*-
"""This module contains the service layer for the Pickles application."""

from datetime import datetime
from zoneinfo import ZoneInfo
from typing import Any, List, Dict
from src.models import Order, Inventory, Customer

class OrderService:
    """Service for handling order-related operations."""
    def __init__(
        self,
        orders_repo: Any,
        customers_repo: Any
    ) -> None:
        self.orders_repo = orders_repo
        self.customers_repo = customers_repo

    def place_order(
        self,
        product_id: int,
        quantity: int,
        customer_id: int,
        is_delivery: bool
    ) -> dict:
        """
        Place a new order and save it to the repository.

        Args:
            product_id: ID of the product to order.
            quantity: Quantity of the product.
            customer_id: ID of the customer placing the order.
            is_delivery: True if delivery, False if pickup.
        Returns:
            dict: Status and order ID.
        """
        vienna_tz = ZoneInfo("Europe/Vienna")
        now = datetime.now(vienna_tz)
        order_id = int(now.timestamp() * 1000)
        order = Order(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            customer_id=customer_id,
            timestamp=now,
            is_delivery=is_delivery
        )
        self.orders_repo.save(OrderService.order_to_dict(order))
        return {"status": "success", "order_id": order_id}

    def list_orders(self) -> List[Dict[str, Any]]:
        """
        List all orders from the repository.

        Returns:
            List of order records.
        """
        return self.orders_repo.load()

    @staticmethod
    def order_to_dict(order: 'Order') -> dict:
        """
        Convert an Order object to a dictionary for storage.

        Args:
            order: The Order instance.
        Returns:
            dict: Dictionary representation of the order.
        """
        return {
            "order_id": order.order_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "customer_id": order.customer_id,
            "timestamp": order.timestamp.isoformat(),
            "is_delivery": order.is_delivery,
        }

    def find_or_register_customer(self, name: str, email: str) -> Customer:
        """
        Find a customer by email or register a new one if not found.

        Args:
            name: Customer name.
            email: Customer email.
        Returns:
            Customer: Customer instance.
        """
        customers = self.customers_repo.load()
        for c in customers:
            if c.get("customer_email") == email:
                return Customer(
                    customer_id=c["customer_id"],
                    customer_name=c["customer_name"],
                    customer_email=c["customer_email"]
                )
        return Customer.register_customer(name, email, self.customers_repo)

    def place_order_for_email(
        self,
        product_id: int,
        quantity: int,
        customer_name: str,
        customer_email: str,
        is_delivery: bool
    ) -> dict:
        """
        Place an order for a customer, registering them if needed.

        Args:
            product_id: ID of the product to order.
            quantity: Quantity of the product.
            customer_name: Name of the customer.
            customer_email: Email of the customer.
            is_delivery: True if delivery, False if pickup.
        Returns:
            dict: Status and order ID.
        """
        customer = self.find_or_register_customer(customer_name, customer_email)
        return self.place_order(
            product_id,
            quantity,
            customer.customer_id,
            is_delivery
        )


class InventoryService:
    """
    Service layer for inventory operations. Handles business logic
    and delegates persistence to the repository.
    """
    def __init__(self, repo: Any) -> None:
        """
        Initialize InventoryService with a repository.

        Args:
            repo: Repository for inventory data.
        """
        self.repo = repo

    def load_inventory(self) -> Inventory:
        """
        Load inventory data and return as an Inventory object.

        Returns:
            Inventory: Inventory instance with current quantities.
        """
        inventory_data = self.repo.load()
        quantities = {
            int(row["product_id"]): int(row["product_quantity"])
            for row in inventory_data
        }
        return Inventory(quantities)

    def add_stock(self, product_id: int, product_key: str, amount: int) -> dict:
        """
        Add stock for a product, saving or updating as needed.

        Args:
            product_id: ID of the product.
            product_key: Key or name of the product.
            amount: Amount to add.
        Returns:
            dict: Status and new quantity.
        """
        inventory = self.load_inventory()
        is_new = inventory.get_stock(product_id) == 0
        inventory.add_stock(product_id, amount)
        if is_new:
            self.repo.save({
                "product_id": product_id,
                "product_key": product_key,
                "product_quantity": amount
            })
        else:
            self.repo.update_quantity(
                product_id, inventory.get_stock(product_id)
            )
        return {
            "status": "success", "new_quantity":
                inventory.get_stock(product_id)
        }

    def reduce_stock(self, product_id: int, amount: int) -> dict:
        """
        Reduce stock for a product, updating the repository.

        Args:
            product_id: ID of the product.
            amount: Amount to reduce.
        Returns:
            dict: Status and new quantity, or error message.
        """
        inventory = self.load_inventory()
        try:
            inventory.reduce_stock(product_id, amount)
        except KeyError:
            return {
                "status": "error", "message": 
                f"Product ID {product_id} not in inventory."
            }
        except ValueError:
            return {
                "status": "error", "message":
                f"Not enough stock for product {product_id}."
            }
        self.repo.update_quantity(product_id, inventory.get_stock(product_id))
        return {
            "status": "success", "new_quantity":
                inventory.get_stock(product_id)
        }
