from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import engine, Base
from routes import vendor_routes, product_routes, po_routes

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ERP Purchase Order Management System",
    description="REST API for managing Vendors, Products, and Purchase Orders",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(vendor_routes.router)
app.include_router(product_routes.router)
app.include_router(po_routes.router)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "ERP PO Management API is running"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}