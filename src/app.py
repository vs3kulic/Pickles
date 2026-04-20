from src.models import Customer
# -*- coding: utf-8 -*-
"""This module contains the setup for the Pickles application."""

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.models import Product, OrderService
from src.inventory import InventoryService
from src.repository import GoogleSheetsRepository, GoogleSheetsConnector
import os

#############
# APP SETUP #
#############

app = FastAPI()

# Serve static files from the 'static' directory
BASE_DIR = os.path.dirname(__file__)
static_dir = os.path.join(BASE_DIR, '..', 'static')
index_path = os.path.join(static_dir, "index.html")
products_path = os.path.join(static_dir, "products.html")
inventory_path = os.path.join(static_dir, "inventory.html")
orders_path = os.path.join(static_dir, "orders.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

###################
# FRONTEND ROUTES #
###################

@app.get("/", response_class=FileResponse)
async def root() -> str:
    return index_path


@app.get("/products", response_class=FileResponse)
async def products() -> str:
    return products_path


@app.get("/inventory", response_class=FileResponse)
async def inventory() -> str:
    return inventory_path


@app.get("/orders", response_class=FileResponse)
async def orders() -> str:
    return orders_path


#########################
# BACKEND API ENDPOINTS #
#########################

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "message": "The Pickles API is available."}


@app.post("/api/products/add")
async def add_product(
    product_id: int = Form(...),
    product_key: str = Form(...),
    product_display_name: str = Form(...),
    product_description: str = Form(...),
    product_is_active: bool = Form(False)
) -> dict:
    repo = GoogleSheetsRepository.get_repo("products")

    product = Product(
        product_id=product_id,
        product_key=product_key,
        product_display_name=product_display_name,
        product_description=product_description,
        product_is_active=product_is_active
    )

    repo.save(product.to_dict())
    return {"status": "success"}


@app.post("/api/inventory/add")
async def add_to_stock(
    product_id: int = Form(...),
    product_key: str = Form(...),
    quantity: int = Form(...)
) -> dict:
    repo = GoogleSheetsRepository.get_repo("inventory")
    service = InventoryService(repo)
    return service.add_stock(product_id, product_key, quantity)


@app.post("/api/inventory/reduce")
async def reduce_stock(
    product_id: int = Form(...),
    quantity: int = Form(...)
) -> dict:
    repo = GoogleSheetsRepository.get_repo("inventory")
    service = InventoryService(repo)
    return service.reduce_stock(product_id, quantity)



# Combined endpoint: create customer if needed, then create order
@app.post("/api/orders/add")
async def add_order(
    product_id: int = Form(...),
    quantity: int = Form(...),
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    is_delivery: bool = Form(False)
) -> dict:
    connector = GoogleSheetsConnector("Pickles DB")
    customers_repo = GoogleSheetsRepository(connector, "customers")
    orders_repo = GoogleSheetsRepository(connector, "orders")

    # Check if customer exists by email
    customers = customers_repo.load()
    customer = None
    for c in customers:
        if c.get("customer_email") == customer_email:
            customer = c
            break
    if customer:
        customer_id = customer["customer_id"]
    else:
        # Register new customer
        result = Customer.register_customer(customer_name, customer_email, customers_repo)
        customer_id = result["customer_id"]

    # Place order
    service = OrderService(orders_repo)
    return service.place_order(product_id, quantity, customer_id, is_delivery)
