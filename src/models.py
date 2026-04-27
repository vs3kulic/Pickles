# -*- coding: utf-8 -*-
"""This module contains the domain models for the Pickles application."""

from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
import uuid


class Product:
    def __init__(self,
                product_id: int,
                product_key: str,
                product_display_name: str | None = None,
                product_description: str | None = None,
                product_is_active: bool = False
    ) -> None:
        self._product_id = product_id
        self._product_key = product_key
        self._product_display_name = product_display_name
        self._product_description = product_description
        self._product_is_active = product_is_active

    def __repr__(self) -> str:
        return f"Product({self._product_id}, '{self._product_key}', {self._product_is_active})"

    def __str__(self) -> str:
        return (
            "Product Details: \n"
            f"{'--'* 14} \n"
            f"Id:           {self._product_id}\n"
            f"Key:          {self._product_key}\n"
            f"Display name: {self._product_display_name}\n"
            f"Description:  {self._product_description}\n"
            f"Is active:    {self._product_is_active}\n"
        )

    def to_dict(self) -> dict:
        return {
        "product_id": self._product_id,
        "product_key": self._product_key,
        "product_display_name": self._product_display_name,
        "product_description": self._product_description,
        "product_is_active": self._product_is_active
        }

    @property
    def product_id(self) -> int:
        return self._product_id

    @property
    def product_key(self) -> str:
        return self._product_key

    @property
    def product_display_name(self) -> str | None:
        return self._product_display_name

    @property
    def product_description(self) -> str | None:
        return self._product_description

    @property
    def product_is_active(self) -> bool:
        return self._product_is_active

    @product_is_active.setter
    def product_is_active(self, value: bool) -> None:
        self._product_is_active = value


@dataclass(frozen=True)
class Order:
    order_id: int
    product_id: int
    quantity: int
    customer_id: int
    timestamp: datetime
    is_delivery: bool

    def __repr__(self) -> str:
        return (f"Order(order_id={self.order_id}, "
                f"product_id={self.product_id}, "
                f"quantity={self.quantity}, "
                f"customer_id={self.customer_id}, "
                f"timestamp={self.timestamp}"
                f"is_delivery={self.is_delivery})")

    def __str__(self) -> str:
        return (
            f"Order Details:\n"
            f"{'--'* 14}\n"
            f"Order ID:     {self.order_id}\n"
            f"Product ID:   {self.product_id}\n"
            f"Quantity:     {self.quantity}\n"
            f"Customer ID:  {self.customer_id}\n"
            f"Timestamp:    {self.timestamp}\n"
            f"Delivery:     {self.is_delivery}\n"
        )


class Inventory:
    def __init__(
        self,
        quantities: dict | None = None,
    ):
        self._quantities = quantities if quantities is not None else {}

    def __repr__(self):
        return f"Inventory(quantities={self._quantities})"

    def add_stock(self, product_id: int, amount: int) -> None:
        self._quantities[product_id] = (
            self._quantities.get(product_id, 0) + amount
    )

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


@dataclass(frozen=True)
class Customer:
    customer_id: str
    customer_name: str
    customer_email: str

    @staticmethod
    def register_customer(name, email, repo):
        customer_id = "customer_" + uuid.uuid4().hex[:8]
        now = datetime.now(ZoneInfo("Europe/Vienna"))
        customer = Customer(
            customer_id=customer_id,
            customer_name=name,
            customer_email=email
        )
        repo.save(customer.to_dict())
        return customer

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
        }
