from pydantic import BaseModel, Field
from typing import List, Optional
from models import POStatus


# ── Vendor ──────────────────────────────────────────────────────────────────

class VendorBase(BaseModel):
    name: str
    contact: str
    rating: Optional[float] = 0.0


class VendorCreate(VendorBase):
    pass


class VendorResponse(VendorBase):
    id: int

    class Config:
        from_attributes = True


# ── Product ──────────────────────────────────────────────────────────────────

class ProductBase(BaseModel):
    name: str
    sku: str
    unit_price: float = Field(gt=0)
    stock_level: Optional[int] = 0


class ProductCreate(ProductBase):
    pass


class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True


# ── PO Items ─────────────────────────────────────────────────────────────────

class POItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    price: float = Field(gt=0)


class POItemResponse(POItemCreate):
    id: int
    po_id: int

    class Config:
        from_attributes = True


# ── Purchase Order ────────────────────────────────────────────────────────────

class POCreate(BaseModel):
    reference_no: str
    vendor_id: int
    status: Optional[POStatus] = POStatus.DRAFT
    items: List[POItemCreate]


class POResponse(BaseModel):
    id: int
    reference_no: str
    vendor_id: int
    total_amount: float
    status: POStatus
    items: List[POItemResponse] = []

    class Config:
        from_attributes = True
