# ERP Purchase Order Management System

A modular FastAPI + PostgreSQL backend for managing Vendors, Products, and Purchase Orders.

---

## Project Structure

```
backend/
├── main.py # App entry point, middleware, router registration
├── database.py # SQLAlchemy engine, session, Base
├── models.py # ORM models (Vendor, Product, PurchaseOrder, PurchaseOrderItem)
├── schemas.py # Pydantic request/response schemas
├── seed.py # Optional: insert sample data
├── requirements.txt
├── .env.example
└── routes/
    ├── __init__.py
    ├── vendor_routes.py # GET /vendors, GET /vendors/{id}, POST /vendors
    ├── product_routes.py # GET /products, GET /products/{id}, POST /products
    └── po_routes.py # GET /purchase-orders, GET /purchase-orders/{id}, POST /purchase-orders
```

---

## Prerequisites

| Tool | Version |
|------------|----------|
| Python | 3.10+ |
| PostgreSQL | 14+ |
| pip | latest |

---

## Setup & Run

### 1. Clone / navigate to the project

```bash
cd backend
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# macOS / Linux
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure the database

Create a PostgreSQL database:

```sql
CREATE DATABASE erp_po_db;
```

Copy the env example and edit as needed:

```bash
cp .env.example .env
```

Default connection string in `.env`:

```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/erp_po_db
```

Update with your PostgreSQL credentials if different.

### 5. Start the server

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Tables are **auto-created** on startup via `Base.metadata.create_all()`.

### 6. (Optional) Seed sample data

```bash
python seed.py
```

---

## API Reference

### Base URL
```
http://localhost:8000
```

### Health
| Method | Endpoint | Description |
|--------|-----------|--------------------|
| GET | `/` | API status |
| GET | `/health` | Health check |

### Vendors
| Method | Endpoint | Description |
|--------|-------------------|--------------------|
| GET | `/vendors` | List all vendors |
| GET | `/vendors/{id}` | Get vendor by ID |
| POST | `/vendors` | Create a vendor |

**POST /vendors — Request Body:**
```json
{
  "name": "Acme Supplies",
  "contact": "acme@example.com",
  "rating": 4.5
}
```

### Products
| Method | Endpoint | Description |
|--------|--------------------|--------------------|
| GET | `/products` | List all products |
| GET | `/products/{id}` | Get product by ID |
| POST | `/products` | Create a product |

**POST /products — Request Body:**
```json
{
  "name": "Laptop",
  "sku": "SKU-001",
  "unit_price": 999.99,
  "stock_level": 50
}
```

### Purchase Orders
| Method | Endpoint | Description |
|--------|-----------------------------|-------------------------|
| GET | `/purchase-orders` | List all POs |
| GET | `/purchase-orders/{id}` | Get PO by ID |
| POST | `/purchase-orders` | Create a PO |

**POST /purchase-orders — Request Body:**
```json
{
  "reference_no": "PO-2024-0001",
  "vendor_id": 1,
  "status": "draft",
  "items": [
    { "product_id": 1, "quantity": 2, "price": 999.99 },
    { "product_id": 2, "quantity": 5, "price": 29.99 }
  ]
}
```

**Response includes auto-calculated total (subtotal + 5% tax):**
```json
{
  "id": 1,
  "reference_no": "PO-2024-0001",
  "vendor_id": 1,
  "total_amount": 2257.47,
  "status": "draft",
  "items": [...]
}
```

**PO Status values:** `draft` | `submitted` | `approved` | `rejected` | `received`

---

## Business Logic

### `calculate_total(items)`

Located in `routes/po_routes.py`. Called automatically on every PO creation.

```
subtotal = Σ (item.quantity × item.price)
tax = subtotal × 0.05
total_amount = subtotal + tax
```

Example:
- 2× Laptop @ $999.99 = $1,999.98
- 5× Mouse @ $29.99 = $149.95
- Subtotal = $2,149.93
- Tax (5%) = $107.50
- **Total = $2,257.43**

---

## Interactive Docs

FastAPI auto-generates interactive documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

---
## Screenshots

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Create Purchase Order
![Create PO](screenshots/create_purchase-order.png)

### API Documentation
![API Docs](screenshots/api-docs.png)

### Database Schema
![Database](screenshots/database.png)

### AI Product Description
![AI-auto description](screenshots/AI-auto description.png)
