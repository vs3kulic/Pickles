# TODO

## Goal
Build a tiny pickle-order app with:
- [x] Static HTML/Tailwind/JS frontend (no Lovable)
- [x] FastAPI backend on Render
- [x] Google Sheets as lightweight persistence

The point is to keep it fun, simple, and backend-focused.


## Stack
- [x] Frontend: Static HTML/CSS/JS (Tailwind via CDN)
- [x] Backend: FastAPI, deployed to Render web service
- [x] Persistence: Google Sheets API for orders + stock


## v1 scope
- [x] One page frontend
- [x] One or two pickle products
- [x] Simple order form
- [ ] Minimal backend API
- [ ] Store orders in Google Sheets
- [ ] Track remaining jar count in Google Sheets


## Frontend
- [x] Create static HTML/CSS/JS form
- [x] Keep UI minimal: product, quantity, name, contact, submit
- [ ] Add frontend call to backend `POST /orders`
- [ ] Add simple success and error messages


## Backend
- [x] Create FastAPI project
- [x] Add basic app structure
- [x] Add `GET /health`
- [ ] Add `GET /products` (next)
- [ ] Add `POST /orders`
- [ ] Validate request data
- [ ] Return clean JSON responses
- [ ] Enable CORS for frontend domain
- [ ] Implement class-based design (`Product`, `Order`, `Inventory`, `OrderService`, `Repository`)


## Google Sheets
- [ ] Create one spreadsheet
- [ ] Add `products` sheet
- [ ] Add `orders` sheet
- [ ] Add `inventory` sheet
- In `products`, store:
  - [ ] product_id
  - [ ] name
  - [ ] active
- In `inventory`, store:
  - [ ] product_id
  - [ ] stock
  - [ ] last_updated
- In `orders`, store:
  - [ ] timestamp
  - [ ] order_id
  - [ ] customer_name
  - [ ] contact
  - [ ] product_id
  - [ ] quantity
  - [ ] status
- [ ] Enable Google Sheets API in Google Cloud
- [ ] Create credentials/service account
- [ ] Share sheet with service account
- [ ] Store credentials securely in backend environment variables


## Order flow
- [ ] Frontend sends order to backend
- [ ] Backend checks product exists
- [ ] Backend checks stock is available
- [ ] Backend appends row to `orders`
- [ ] Backend updates stock in `products`
- [ ] Backend returns success or out-of-stock response


## Render
- [x] Create backend repo
- [x] Push FastAPI code to GitHub
- [x] Create Render web service from repo
- [ ] Add environment variables for Google credentials
- [ ] Deploy and test public API URL


## Nice-to-have later
- [ ] Admin endpoint to list orders
- [ ] Admin endpoint to restock jars
- [ ] Basic order status handling
- [ ] Simple auth for admin routes
- [ ] Better form validation
- [ ] Friendly confirmation page
- [ ] Basic logging


## Keep it simple, stupid
- [ ] No Postgres
- [ ] No auth in v1
- [ ] No payments
- [ ] No fancy inventory logic
- [ ] No overengineering


## Definition of done
- [ ] Public frontend is live
- [ ] Backend is live
- [ ] User can submit pickle order
- [ ] Order lands in Google Sheets
- [ ] Stock count decreases correctly
- [ ] Every function has >= 1 unit tests
