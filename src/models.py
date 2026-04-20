import uuid


# -*- coding: utf-8 -*-
from dataclasses import dataclass
from datetime import datetime
from zoneinfo import ZoneInfo
from src.repository import GoogleSheetsConnector, GoogleSheetsRepository

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


# ====================
# Task 3: Order Service
# ====================
# [ ] Implement an OrderService class with:
#     - Fields: repository (repository instance)
#     - Methods: place_order(product_id, quantity, customer_id, is_delivery)
#     - Methods: list_orders()
# [ ] __init__ method to set the repository
# [ ] to_dict() -> dict: returns a dictionary representation
# [ ] from_dict(data: dict) -> OrderService: classmethod to create an OrderService from a dict
# [ ] __repr__ or __str__ for debugging
# [ ] Getters and setters for fields (use @property for status, quantity, etc.)
# [ ] Static method: validate_status(status: str) -> bool
# [ ] Class method: generate_order_id() -> str
# [ ] (Optional) Abstract base class for shared model methods (e.g., to_dict, from_dict)


class OrderService:

    def __init__(self, repo):
        self.repo = repo

    def place_order(self,
                    product_id,
                    quantity,
                    customer_id,
                    is_delivery
    ) -> dict:
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
        self.repo.save(OrderService.order_to_dict(order))
        return {"status": "success", "order_id": order_id}

    def list_orders(self):
        return self.repo.load()

    @staticmethod
    def order_to_dict(order: 'Order') -> dict:
        return {
            "order_id": order.order_id,
            "product_id": order.product_id,
            "quantity": order.quantity,
            "customer_id": order.customer_id,
            "timestamp": order.timestamp.isoformat(),
            "is_delivery": order.is_delivery,
        }

    @staticmethod
    def place_order_for_email(product_id, quantity, customer_name, customer_email, is_delivery):
        connector = GoogleSheetsConnector("Pickles DB")
        customers_repo = GoogleSheetsRepository(connector, "customers")
        orders_repo = GoogleSheetsRepository(connector, "orders")

        # Find or create customer
        customers = customers_repo.load()
        customer = None
        for c in customers:
            if c.get("customer_email") == customer_email:
                customer = c
                break
        if customer:
            customer_id = customer["customer_id"]
        else:
            result = Customer.register_customer(customer_name, customer_email, customers_repo)
            customer_id = result["customer_id"]

        # Place order
        service = OrderService(orders_repo)
        return service.place_order(product_id, quantity, customer_id, is_delivery)


@dataclass(frozen=True)
class Customer:
    customer_id: str
    customer_name: str
    customer_email: str

    @staticmethod
    def register_customer(name, email, repo):
        customer_id = uuid.uuid4().hex
        now = datetime.now(ZoneInfo("Europe/Vienna"))
        repo.save({
            "customer_id": customer_id,
            "customer_name": name,
            "customer_email": email
        })
        return {"status": "success", "customer_id": customer_id}

    def to_dict(self):
        return {
            "customer_id": self.customer_id,
            "customer_name": self.customer_name,
            "customer_email": self.customer_email,
        }
