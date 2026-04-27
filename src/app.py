# -*- coding: utf-8 -*-
"""This module contains the setup and endpoints for the Pickles application."""

import os
from fastapi import FastAPI, Form, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse
from src.dependencies import build_product_service, build_inventory_service, build_order_service

#############
# APP SETUP #
#############

app = FastAPI()

# Serve static files from the 'static' directory
BASE_DIR = os.path.dirname(__file__)
static_dir = os.path.join(BASE_DIR, '..', 'static')
index_path = os.path.join(static_dir, "index.html")
inventory_path = os.path.join(static_dir, "inventory.html")
orders_path = os.path.join(static_dir, "orders.html")
success_path = os.path.join(static_dir, "success.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

###################
# FRONTEND ROUTES #
###################

@app.get("/", response_class=FileResponse)
async def root() -> str:
    return index_path


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

#
# Products
#

class ProductResponse(BaseModel):
    product_id: int
    product_key: str
    product_display_name: str | None = None
    product_description: str | None = None
    product_is_active: bool

# API response will be a JSON array (list) of objects
# Each object in the array matches the ProductResponse schema
@app.get("/api/products", response_model=list[ProductResponse])
async def get_products():
    service = build_product_service()
    product = service.list_products()
    return product


class ProductCreateRequest(BaseModel):
    """Pydantic model for parsing and validating incoming API data."""
    product_id: int
    product_key: str
    product_display_name: str | None = None
    product_description: str | None = None
    product_is_active: bool = False

@app.post("/api/products/add")
async def add_product(request: ProductCreateRequest) -> dict:
    service = build_product_service()
    return service.add_product(
        product_id=request.product_id,
        product_key=request.product_key,
        product_display_name=request.product_display_name,
        product_description=request.product_description,
        product_is_active=request.product_is_active
    )

#
# Inventory
#

@app.post("/api/inventory/add")
async def add_to_stock(
    product_id: int = Form(...),
    product_key: str = Form(...),
    quantity: int = Form(...)
) -> dict:
    service = build_inventory_service()
    result = service.add_stock(product_id, product_key, quantity)
    return result


@app.post("/api/inventory/reduce")
async def reduce_stock(
    product_id: int = Form(...),
    quantity: int = Form(...)
) -> dict:
    service = build_inventory_service()
    return service.reduce_stock(product_id, quantity)

#
# Orders
#

@app.post("/api/orders/add")
async def add_order(
    product_id: int = Form(...),
    quantity: int = Form(...),
    customer_name: str = Form(...),
    customer_email: str = Form(...),
    is_delivery: bool = Form(False)
):
    service = build_order_service()
    result = service.place_order_for_email(
        product_id=product_id,
        quantity=quantity,
        customer_name=customer_name,
        customer_email=customer_email,
        is_delivery=is_delivery,
    )
    if result.get("status") == "success":
        return RedirectResponse(url="/static/success.html", status_code=303)
    raise HTTPException(
        status_code=400,
        detail=result.get("message", "Order could not be placed.")
    )
