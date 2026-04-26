# TODO

## Goal
Build a tiny pickle-order app with:
- [x] Static HTML/Tailwind/JS frontend
- [x] FastAPI backend on Render
- [x] Google Sheets as lightweight persistence

The point is to keep it fun, simple, and backend-focused.

## Stack
- [x] Frontend: Static HTML/CSS/JS
- [x] Backend: FastAPI, deployed to Render web service
- [x] Persistence: Google Sheets API via `gspread`

## Current scope
- [x] Multiple frontend pages (`/`, `/products`, `/inventory`, `/orders`)
- [x] Product creation flow
- [x] Inventory add/reduce flow
- [x] Order submission flow
- [x] Customer registration / lookup by email
- [x] Google Sheets persistence for products, inventory, orders, and customers
- [x] Basic service + repository layering

## Frontend
- [x] Static pages for landing, products, inventory, and orders
- [x] Minimal forms for product, inventory, and order actions
- [ ] Improve form success/error feedback
- [ ] Add friendlier confirmation UX for order submission
- [ ] Tighten styling / landing page polish
- [ ] Consider simple multi-language support later

## Backend
- [x] Create FastAPI project
- [x] Add app structure
- [x] Add `GET /health`
- [x] Add `POST /api/products/add`
- [x] Add `POST /api/inventory/add`
- [x] Add `POST /api/inventory/reduce`
- [x] Add `POST /api/orders/add`
- [x] Implement domain models (`Product`, `Order`, `Inventory`, `Customer`)
- [x] Implement service layer (`InventoryService`, `OrderService`)
- [x] Implement repository abstraction + Google Sheets repository
- [x] Add `ProductService` for consistency
- [ ] Standardize dependency wiring (`dependencies.py` / `Depends`)
- [ ] Standardize error handling strategy
- [ ] Return cleaner, more consistent API responses
- [ ] Add request validation where business rules are still implicit
- [ ] Enable CORS if frontend/backend are split across domains

## Google Sheets
- [x] Create spreadsheet
- [x] Add `products` sheet
- [x] Add `inventory` sheet
- [x] Add `orders` sheet
- [x] Add `customers` sheet
- [x] Enable Google Sheets API in Google Cloud
- [x] Create service account credentials
- [x] Share spreadsheet with service account
- [x] Store credentials via environment variable

### Current sheet structure
- `products`
  - [x] `product_id`
  - [x] `product_key`
  - [x] `product_display_name`
  - [x] `product_description`
  - [x] `product_is_active`

- `inventory`
  - [x] `product_id`
  - [x] `product_key`
  - [x] `product_quantity`

- `customers`
  - [x] `customer_id`
  - [x] `customer_name`
  - [x] `customer_email`

- `orders`
  - [x] `order_id`
  - [x] `product_id`
  - [x] `quantity`
  - [x] `customer_id`
  - [x] `timestamp`
  - [x] `is_delivery`

## Order flow
- [x] Frontend sends order form to backend
- [x] Backend creates or finds customer by email
- [x] Backend appends row to `orders`
- [ ] Backend checks product exists before placing order
- [ ] Backend checks stock before placing order
- [ ] Backend reduces inventory automatically when an order is placed
- [ ] Backend returns clearer business-error responses
- [ ] Show success page / failure message cleanly in the UI

## Render
- [x] Create backend repo
- [x] Push FastAPI code to GitHub
- [x] Create Render web service from repo
- [x] Add environment variables for Google credentials
- [x] Deploy and test public API URL

## Nice-to-have later
- [ ] Admin endpoint to list orders
- [ ] Admin endpoint to list products
- [ ] Admin endpoint to restock inventory
- [ ] Product activation/deactivation flow in UI
- [ ] Basic order status handling
- [ ] Better logging
- [ ] Unit tests for services
- [ ] Integration tests for API routes
- [ ] Swap Google Sheets for SQL later if useful

## Keep it simple, stupid
- [x] No Postgres for v1
- [x] No auth for v1
- [x] No payments
- [x] No fancy inventory logic
- [x] No overengineering

## Definition of done
- [x] Backend is live
- [x] User can create products
- [x] User can manage stock manually
- [x] User can submit pickle orders
- [x] Order lands in Google Sheets
- [ ] Stock count decreases automatically on order
- [ ] Product existence is validated on order
- [ ] Out-of-stock orders are blocked
- [ ] Core service functions have unit tests
- [ ] Frontend is polished enough to share without apology
