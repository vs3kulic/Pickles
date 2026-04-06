# Planned Classes

Five classes with separated concerns.

---

## `Product` -> `models.py`

Represents one pickle product in the inventory.

**Fields:** `product_id`, `name`, `price`, `stock`, `active`

**Methods:**
- `is_in_stock(quantity)` -> bool
- `decrease_stock(quantity)` -> None
- `increase_stock(quantity)` -> None

---

## `Order` -> `models.py`

Represents one customer order.

**Fields:** `order_id`, `customer_name`, `contact`, `product_id`, `quantity`, `timestamp`, `status`

**Methods:**
- `to_dict()` -> dict
- `from_dict(data)` -> Order *(classmethod)*

---

## `Inventory` -> `inventory.py`

Manages the collection of products and stock logic.

**Methods:**
- `get_product(product_id)` -> Product
- `list_products()` -> list[Product]
- `can_fulfill(product_id, quantity)` -> bool
- `reserve(product_id, quantity)` -> None

---

## `OrderService` -> `services.py`

The brain. Coordinates inventory and persistence to handle the "place an order" use case.

**Methods:**
- `get_products()` -> list[Product]
- `place_order(customer_name, contact, product_id, quantity)` -> Order

**Flow:**
1. Check product exists
2. Check stock via Inventory
3. Create Order
4. Reserve stock
5. Save order via Repository

---

## `Repository` -> `repositories.py`

Storage layer. Abstract base class. Start with `JsonRepository`, swap to `GoogleSheetsRepository` later without touching the service.

**Abstract methods:**
- `load_products()` -> list
- `save_products(products)` -> None
- `load_orders()` -> list
- `save_order(order)` -> None

**Concrete implementations:**
- `JsonRepository` â€” reads/writes `products.json` and `orders.json`
- `GoogleSheetsRepository` â€” reads/writes Google Sheets via API *(later)*

---

## Rule of thumb

| Class          | Knows about                    |
|--------------- |--------------------------------|
| `Product`      | Product data, stock rules      |
| `Order`        | Order data                     |
| `Inventory`    | Collection of products         |
| `OrderService` | Business logic                 |
| `Repository`   | Storage only                   |

`OrderService` talks to `Inventory` and `Repository`. Routes talk to `OrderService`. Nothing else crosses those lines.