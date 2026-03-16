from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import PurchaseOrder, PurchaseOrderItem, Vendor, Product
from schemas import POCreate, POResponse

router = APIRouter(prefix="/purchase-orders", tags=["Purchase Orders"])

TAX_RATE = 0.05 # 5% tax


def calculate_total(items: List[PurchaseOrderItem]) -> float:
    """
    Calculate the total amount for a Purchase Order.
    - Sums quantity * price for all line items
    - Applies 5% tax automatically
    - Returns the final total_amount (subtotal + tax)
    """
    subtotal = sum(item.quantity * item.price for item in items)
    tax = subtotal * TAX_RATE
    total = round(subtotal + tax, 2)
    return total


@router.get("/", response_model=List[POResponse])
def get_purchase_orders(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        orders = db.query(PurchaseOrder).offset(skip).limit(limit).all()
        return orders
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch purchase orders: {str(e)}"
        )


@router.get("/{po_id}", response_model=POResponse)
def get_purchase_order(po_id: int, db: Session = Depends(get_db)):
    try:
        order = db.query(PurchaseOrder).filter(PurchaseOrder.id == po_id).first()
        if not order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Purchase Order with id {po_id} not found"
            )
        return order
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch purchase order: {str(e)}"
        )


@router.post("/", response_model=POResponse, status_code=status.HTTP_201_CREATED)
def create_purchase_order(po: POCreate, db: Session = Depends(get_db)):
    try:
        # Validate vendor exists
        vendor = db.query(Vendor).filter(Vendor.id == po.vendor_id).first()
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {po.vendor_id} not found"
            )

        # Validate reference_no uniqueness
        existing = db.query(PurchaseOrder).filter(
            PurchaseOrder.reference_no == po.reference_no
        ).first()
        if existing:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Purchase Order with reference '{po.reference_no}' already exists"
            )

        # Validate all products exist
        if not po.items:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Purchase Order must have at least one item"
            )

        for item_data in po.items:
            product = db.query(Product).filter(Product.id == item_data.product_id).first()
            if not product:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Product with id {item_data.product_id} not found"
                )

        # Create the PO record
        db_po = PurchaseOrder(
            reference_no=po.reference_no,
            vendor_id=po.vendor_id,
            status=po.status,
            total_amount=0.0
        )
        db.add(db_po)
        db.flush() # get db_po.id before committing

        # Create PO items
        db_items = []
        for item_data in po.items:
            db_item = PurchaseOrderItem(
                po_id=db_po.id,
                product_id=item_data.product_id,
                quantity=item_data.quantity,
                price=item_data.price
            )
            db.add(db_item)
            db_items.append(db_item)

        db.flush() # persist items so calculate_total can use them

        # Apply business logic: calculate total with 5% tax
        db_po.total_amount = calculate_total(db_items)

        db.commit()
        db.refresh(db_po)
        return db_po

    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create purchase order: {str(e)}"
        )