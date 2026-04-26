
# Pickles

A minimal FastAPI app for managing spicy pickle orders, built for learning and fun.

![Python](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)
![FastAPI](https://img.shields.io/badge/fastapi-0.110%2B-green?logo=fastapi)
![Status](https://img.shields.io/badge/status-experimental-orange)

## Features

- Place and track pickle orders
- Manage products and inventory
- Simple web forms and API endpoints
- Data persistence via Google Sheets

## Stack

- FastAPI (web framework)
- Python 3.10+
- Google Sheets (via gspread)
- Uvicorn (ASGI server)
- HTML + Tailwind CSS (static frontend)

## Architecture

- **FastAPI app & routes:** Handles web and API endpoints for products, inventory, and orders.
- **Models:** Product, Order, Inventory, Customer (define core data structures).
- **Services:** Business logic layer for products, inventory, and orders.
- **Repository layer:** Abstracts data access, currently using Google Sheets as the backend.

## Setup

```bash
git clone https://github.com/vs3kulic/Pickles.git
cd Pickles
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

> **Note:**  
> You need a Google service account and must set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to your credentials JSON file for Google Sheets access.

## Run locally

```bash
uvicorn app:app --reload
```

- Home: [http://localhost:8000/](http://localhost:8000/)
- Products: [http://localhost:8000/products](http://localhost:8000/products)
- Inventory: [http://localhost:8000/inventory](http://localhost:8000/inventory)
- Orders: [http://localhost:8000/orders](http://localhost:8000/orders)
- API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Why this project exists

Pickles is a small learning project to explore modern Python web development, layered architecture, and a real-world workflow (taking and managing pickle orders) in a simple, approachable way.

---

Ps: the pickles are real! 🥒🔥
