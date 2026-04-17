# -*- coding: utf-8 -*-

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

class Order:
    
    def __init__(self, 
                first_name: str,
                last_name: str,
                ordered_product: str,
                ordered_quantity: int,
                is_delivery: bool = False
    ) -> None:
        self._first_name = first_name
        self._last_name = last_name
        self._ordered_product = ordered_product
        self._ordered_quantity = ordered_quantity
        self._is_delivery = is_delivery

    def __repr__(self) -> str:
        return (f"Order(first_name={self._first_name}, "
                f"last_name={self._last_name}, "
                f"ordered_product={self._ordered_product}, "
                f"quantity={self._ordered_quantity}, "
                f"delivery={self._is_delivery})"
        )

    def __str__(self) -> str:
        return (
            "Product Details: \n"
            f"{'--'* 14} \n"
            f"First name:   {self._first_name}\n"
            f"Last name:    {self._last_name}\n"
            f"Product:      {self._ordered_product}\n"
            f"Quantity:     {self._ordered_quantity}\n"
            f"Delivery:     {self._is_delivery}\n"
        )

    @property
    def first_name(self) -> str:
        return self._first_name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def ordered_product(self) -> str:
        return self._ordered_product

    @property
    def ordered_quantity(self) -> int:
        return self._ordered_quantity

    @property
    def is_delivery(self) -> bool:
        return self._is_delivery

    @is_delivery.setter
    def is_delivery(self, value: bool) -> None:
        self._is_delivery = value


def main():
    """Main function to demo the models."""
    # Product demo
    p1 = Product("4", "gnarly_pickles", product_is_active=False)
    print(repr(p1))
    p1.product_is_active = True
    print(p1)

    # Order demo
    pass

if __name__ == "__main__":
    main()
