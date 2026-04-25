# -*- coding: utf-8 -*-
"""This module contains the utils for the Pickles application."""

from src.services import ProductService, InventoryService, OrderService
from src.repository import GoogleSheetsRepository, GoogleSheetsConnector


def build_product_service() -> ProductService:
    connector = GoogleSheetsConnector("Pickles DB")
    products_repo = GoogleSheetsRepository(connector, "products")
    return ProductService(products_repo)


def build_inventory_service() -> InventoryService:
    connector = GoogleSheetsConnector("Pickles DB")
    inventory_repo = GoogleSheetsRepository(connector, "inventory")
    return InventoryService(inventory_repo)


def build_order_service() -> OrderService:
    connector = GoogleSheetsConnector("Pickles DB")
    customers_repo = GoogleSheetsRepository(connector, "customers")
    orders_repo = GoogleSheetsRepository(connector, "orders")
    return OrderService(orders_repo, customers_repo)
