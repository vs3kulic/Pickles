# -*- coding: utf-8 -*-

# =====================
# Task 1: Product Class
# =====================
# [x] Implement a Product class with:
#     - Fields: product_id (str), product_name (str), product_display_name (str), product_description (str), product_is_active (bool)
#     - Note: stock is managed by the Inventory class, not here
# [x] __init__ method to set all fields
# [x] __repr__ and __str__ for debugging
# [ ] to_row() -> list: returns data as a list matching sheet column order (for gspread writes)
# [ ] to_dict() -> dict: returns data as a dict matching sheet column names (for API responses)
# [ ] Class method: from_dict(data: dict) -> Product (handle active: 1/0 -> bool conversion)
# [ ] Getters and setters for fields (use @property)
# [ ] Static method: validate_product_data(data: dict) -> bool

class Product:
    
    def __init__(self,
                product_id: str,
                product_name: str,
                product_display_name: str | None = None,
                product_description: str | None = None,
                product_is_active: bool = True
    ) -> None:
        self._product_id = product_id
        self._product_name = product_name
        self._product_display_name = product_display_name
        self._product_description = product_description
        self._product_is_active = product_is_active

    def __repr__(self) -> str:
        return f"Product('{self._product_id}', ‘{self._product_name}‘, {self._product_is_active})"

    def __str__(self) -> str:
        return (
            "Product Details: \n"
            f"{'--'* 14} \n"
            f"Id:           {self._product_id} \n"
            f"Name:         {self._product_name} \n"
            f"Display name: {self._product_display_name} \n"
            f"Description:  {self._product_description} \n"
            f"Is active:    {self._product_is_active} \n"
        )


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


def main():
    """Main function to demo the models."""
    p1 = Product("4", "gnarly_pickles", product_is_active=False)
    print(repr(p1))
    print(p1)

if __name__ == "__main__":
    main()
