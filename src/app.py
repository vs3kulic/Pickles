# -*- coding: utf-8 -*-
"""This module contains the setup for the Pickles application."""

from fastapi import FastAPI, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.repository import GoogleSheetsConnector, GoogleSheetsRepository
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


#########################
# BACKEND API ENDPOINTS #
#########################

@app.get("/health")
async def health() -> dict:
    return {"status": "ok", "message": "The Pickles API is available."}


@app.post("/api/products")
async def add_product(
    product_id: int = Form(...),
    product_key: str = Form(...),
    product_display_name: str = Form(...),
    product_description: str = Form(...),
    product_is_active: bool = Form(False)
) -> dict:
    connector = GoogleSheetsConnector("Pickles DB")
    repo = GoogleSheetsRepository(connector, "products")
    repo.save({
            "product_id": product_id,
            "product_key": product_key,
            "product_display_name": product_display_name,
            "product_description": product_description,
            "product_is_active": product_is_active
    })
    return {"status": "success"}


@app.post("/api/inventory/add")
async def add_to_stock(
    product_id: int = Form(...),
    product_key: str = Form(...),
    product_quantity: int = Form(...)
) -> dict:
    connector = GoogleSheetsConnector("Pickles DB")
    repo = GoogleSheetsRepository(connector, "inventory")
    repo.save({
        "product_id": product_id,
        "product_key": product_key,
        "product_quantity": product_quantity
    })
    return {"status": "success"}


@app.post("/api/inventory/reduce")
async def reduce_stock(
    product_id: int = Form(...),
    product_key: str = Form(...),
    reduce_quantity: int = Form(...)
) -> dict:
    connector = GoogleSheetsConnector("Pickles DB")
    repo = GoogleSheetsRepository(connector, "inventory")
    # TODO: implement logic to find the row and update product_quantity
    # (not just append a new row)
    # Example: load all, find product_id, update quantity, write back
    return {"status": "success"}
