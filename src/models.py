# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime

# =====================
# Task 1: Product Class
# =====================
# [ ] Class method: from_dict(data: dict) -> Product (handle active: 1/0 -> bool conversion)
# [ ] Static method: validate_product_data(data: dict) -> bool

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


# ====================
# Task 2: Order Class
# ====================
# [ ] Implement an Order class with:
#     - Fields: order_id (str), customer_name (str), contact (str), product_id (str), quantity (int), timestamp (datetime), status (str)
# [ ] __init__ method to set all fields
# [ ] to_dict() -> dict: returns a dictionary representation
# [ ] from_dict(data: dict) -> Order: classmethod to create an Order from a dict
# [ ] __repr__ or __str__ for debugging
# [ ] Getters and setters for fields (use @property for status, quantity, etc.)
# [ ] Static method: validate_status(status: str) -> bool
# [ ] Class method: generate_order_id() -> str
# [ ] (Optional) Abstract base class for shared model methods (e.g., to_dict, from_dict)


@dataclass(frozen=True)
class Order:
    order_id: int
    product_id: int
    quantity: int
    customer_id: int
    timestamp: datetime
    is_delivery: bool

    def __repr__(self) -> str:
        return (f"Order(order_id={self.order_id}, product_id={self.product_id}, "
                f"quantity={self.quantity}, customer_id={self.customer_id}, "
                f"is_delivery={self.is_delivery})")

    def __str__(self) -> str:
        return (
            f"Order Details:\n"
            f"{'--'* 14}\n"
            f"Order ID:     {self.order_id}\n"
            f"Product ID:   {self.product_id}\n"
            f"Quantity:     {self.quantity}\n"
            f"Customer ID:  {self.customer_id}\n"
            f"Delivery:     {self.is_delivery}\n"
        )
