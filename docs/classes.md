# Classes Overview
# Classes Overview

This document describes the object-oriented structure of the Pickles application. The codebase is organized in a layered architecture: **domain models**, **repository layer**, **service layer**, and **FastAPI endpoints**. Each class below is documented with its responsibility, fields, methods, and relationships to other classes.

---

## Architecture at a glance

```
+------------------------------------------------------------+
|                        Client / Browser                    |
+------------------------------------------------------------+
                             |
                             v
+------------------------------------------------------------+
|                 FastAPI Application (main.py)              |
|  Frontend routes:   /, /products, /inventory, /orders      |
|  API endpoints:     /api/products/add                      |
|                     /api/inventory/add                     |
|                     /api/inventory/reduce                  |
|                     /api/orders/add                        |
+------------------------------------------------------------+
                             |
                             v
+------------------------------------------------------------+
|                      Service Layer                         |
|   OrderService          InventoryService                   |
+------------------------------------------------------------+
                             |
                             v
+------------------------------------------------------------+
|                     Domain Models                          |
|  Product   Order   Inventory   Customer                    |
+------------------------------------------------------------+
                             |
                             v
+------------------------------------------------------------+
|                    Repository Layer                        |
|  Repository (ABC)                                          |
|    └── GoogleSheetsRepository                              |
|            uses GoogleSheetsConnector                      |
+------------------------------------------------------------+
                             |
                             v
+------------------------------------------------------------+
|                       Google Sheets                        |
|   worksheets: products | inventory | orders | customers    |
+------------------------------------------------------------+
```

---

## Domain Models (`src/models.py`)

### Product

Represents a product in the catalog.

```
+----------------------------------------------+
| Product                                      |
+----------------------------------------------+
| - _product_id: int                           |
| - _product_key: str                          |
| - _product_display_name: str | None          |
| - _product_description: str | None           |
| - _product_is_active: bool                   |
+----------------------------------------------+
| + to_dict() -> dict                          |
| + properties: product_id, product_key,       |
|   product_display_name, product_description, |
|   product_is_active (get/set)                |
+----------------------------------------------+
```

- Encapsulates product attributes with private fields and read-only properties.
- `product_is_active` is the only mutable property.
- `to_dict()` is used by the repository layer when persisting to Google Sheets.

---

### Order

Immutable record of a placed order, implemented as a frozen dataclass.

```
+----------------------------------------------+
| Order (frozen dataclass)                     |
+----------------------------------------------+
| + order_id: int                              |
| + product_id: int                            |
| + quantity: int                              |
| + customer_id: int                           |
| + timestamp: datetime                        |
| + is_delivery: bool                          |
+----------------------------------------------+
```

- Fields are set once at construction; the frozen dataclass prevents mutation.
- Serialization to a dict happens in `OrderService.order_to_dict()`, not on the model itself.

---

### Inventory

Represents current stock quantities by product ID.

```
+----------------------------------------------+
| Inventory                                    |
+----------------------------------------------+
| - _quantities: dict[int, int]                |
+----------------------------------------------+
| + add_stock(product_id, amount)              |
| + get_stock(product_id) -> int               |
| + reduce_stock(product_id, amount=1)         |
| + list_inventory() -> list[tuple]            |
+----------------------------------------------+
```

- `reduce_stock()` raises `KeyError` if the product is missing and `ValueError` if there is not enough stock.
- `get_stock()` returns `0` for unknown products.

---

### Customer

Immutable customer entity, implemented as a frozen dataclass.

```
+----------------------------------------------+
| Customer (frozen dataclass)                  |
+----------------------------------------------+
| + customer_id: str                           |
| + customer_name: str                         |
| + customer_email: str                        |
+----------------------------------------------+
| + register_customer(name, email, repo)       |
|   [static] -> Customer                       |
| + to_dict() -> dict                          |
+----------------------------------------------+
```

- `register_customer()` generates a UUID-based `customer_id`, instantiates the Customer, and calls `repo.save()` directly.
- This is the one place a model talks to a repository.

---

## Repository Layer (`src/repository.py`)

### Repository (ABC)

Abstract base class defining the persistence contract.

```
+----------------------------------------------+
| Repository (abstract)                        |
+----------------------------------------------+
| - _name: str                                 |
+----------------------------------------------+
| + load() -> list[dict]            [abstract] |
| + save( dict) -> None        [abstract] |
| + update_quantity(product_id,                |
|                   new_quantity)   [abstract] |
+----------------------------------------------+
```

Subclasses must implement all three methods.

---

### GoogleSheetsConnector

Authenticates with Google and opens a worksheet document.

```
+----------------------------------------------+
| GoogleSheetsConnector                        |
+----------------------------------------------+
| - _document: str                             |
| - _gdoc: Spreadsheet                         |
+----------------------------------------------+
| - _authenticate() -> gspread.Client          |
| + get_worksheet(name) -> Worksheet           |
+----------------------------------------------+
```

- Reads credentials from the `GOOGLE_APPLICATION_CREDENTIALS` environment variable.
- Raises `ValueError` when a worksheet is missing from the document.

---

### GoogleSheetsRepository

Concrete `Repository` backed by a single Google Sheets worksheet.

```
+----------------------------------------------+
| GoogleSheetsRepository : Repository          |
+----------------------------------------------+
| - _connector: GoogleSheetsConnector          |
| - _worksheet: Worksheet                      |
+----------------------------------------------+
| + load() -> list[dict]                       |
| + save( dict) -> None                   |
| + update_quantity(product_id, new_quantity)  |
| + get_repo(entity) [static]                  |
|   -> GoogleSheetsRepository                  |
+----------------------------------------------+
```

- `load()` returns rows as dicts keyed by header row.
- `save()` aligns dict keys to the worksheet header row before appending.
- `update_quantity()` locates the matching product row and updates the `product_quantity` cell.
- `get_repo()` is a convenience factory that creates a connector for the `Pickles DB` document and returns a repository bound to the given entity worksheet.

---

## Service Layer (`src/services.py`)

### OrderService

Coordinates order placement and customer registration.

```
+----------------------------------------------+
| OrderService                                 |
+----------------------------------------------+
| + orders_repo                                |
| + customers_repo                             |
+----------------------------------------------+
| + place_order(product_id, quantity,          |
|               customer_id, is_delivery)      |
| + list_orders() -> list[dict]                |
| + find_or_register_customer(name, email)     |
|   -> Customer                                |
| + place_order_for_email(product_id,          |
|     quantity, customer_name,                 |
|     customer_email, is_delivery)             |
| + order_to_dict(order) [static] -> dict      |
+----------------------------------------------+
```

- Depends on two repository instances, injected via the constructor.
- `order_id` is generated from the current Vienna-timezone timestamp in milliseconds.
- `find_or_register_customer()` loads existing customers and either reconstructs a `Customer` from a matching record or delegates to `Customer.register_customer()`.
- `place_order_for_email()` is the main orchestration method used by the API endpoint.

---

### InventoryService

Coordinates stock updates on the inventory worksheet.

```
+----------------------------------------------+
| InventoryService                             |
+----------------------------------------------+
| + repo                                       |
+----------------------------------------------+
| + load_inventory() -> Inventory              |
| + add_stock(product_id, product_key, amount) |
|   -> dict                                    |
| + reduce_stock(product_id, amount) -> dict   |
+----------------------------------------------+
```

- `load_inventory()` builds an `Inventory` in memory from the repository rows.
- `add_stock()` decides between a new row (save) and an existing row (update quantity).
- `reduce_stock()` catches missing products and insufficient stock and returns structured error dicts instead of raising.

---

## FastAPI Application (`main.py`)

### Frontend routes

Serve static HTML pages from the `static/` directory.

```
GET /            -> static/index.html
GET /products    -> static/products.html
GET /inventory   -> static/inventory.html
GET /orders      -> static/orders.html
```

### Backend API endpoints

```
GET  /health                  -> API health check
POST /api/products/add        -> add a new Product
POST /api/inventory/add       -> increase stock for a product
POST /api/inventory/reduce    -> decrease stock for a product
POST /api/orders/add          -> place a new order
```

Endpoints instantiate the connector, build the needed `GoogleSheetsRepository` instances, wire them into the appropriate service, and delegate business logic to the service layer.

---

## Relationships between classes

```
+-------------------+         implements
|   Repository(ABC) | <----------------------+
+-------------------+                        |
                                             |
                                             |
                              +--------------+-----------+
                              | GoogleSheetsRepository   |
                              +--------------------------+
                                             |
                                   uses      v
                              +--------------------------+
                              | GoogleSheetsConnector    |
                              +--------------------------+
                                             |
                                             v
                                     +---------------+
                                     | Google Sheets |
                                     +---------------+


   +------------------+    creates    +---------+
   |   OrderService   | ------------> |  Order  |
   +------------------+               +---------+
          |  |                          
          |  |  finds / registers       
          |  +------------------->  +----------+
          |                          | Customer |
          |                          +----------+
          |                                ^
          |  persists via both             |  register_customer
          v                                |  saves via repo
   +------------------------+              |
   | GoogleSheetsRepository | <------------+
   +------------------------+


   +---------------------+    manages    +------------+
   |  InventoryService   | ------------> | Inventory  |
   +---------------------+               +------------+
                 |
                 |   persists via
                 v
         +------------------------+
         | GoogleSheetsRepository |
         +------------------------+
```

---

## Design notes

- **Layered architecture.** Route handlers stay thin; services coordinate workflows; repositories own persistence; models hold data and minimal behavior.
- **Dependency injection.** Services receive repository instances via their constructors, making them easy to swap or test.
- **Abstract persistence.** `Repository` defines the contract; `GoogleSheetsRepository` is the only current implementation, but additional backends can be added without touching services.
- **Timezone-aware timestamps.** Both `OrderService.place_order` and `Customer.register_customer` use `ZoneInfo("Europe/Vienna")` for accurate local time.
- **Immutable vs mutable models.** `Order` and `Customer` are frozen dataclasses; `Product` and `Inventory` are mutable because their state legitimately changes over time.
````

