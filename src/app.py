# -*- coding: utf-8 -*-

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
admin_path = os.path.join(static_dir, "admin.html")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

#################
# API ENDPOINTS #
#################

@app.get("/", response_class=FileResponse)
async def root():
    return index_path


@app.get("/admin", response_class=FileResponse)
async def admin():
    return admin_path


@app.get("/health")
async def health():
    return {"status": "ok", "message": "The Pickles API is available."}


@app.post("/api/products")
async def add_product(
    product_id: int = Form(...),
    product_key: str = Form(...),
    product_display_name: str = Form(...),
    product_description: str = Form(...),
    product_is_active: bool = Form(False)
):
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