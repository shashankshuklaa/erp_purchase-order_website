from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models import Vendor
from schemas import VendorCreate, VendorResponse

router = APIRouter(prefix="/vendors", tags=["Vendors"])


@router.get("/", response_model=List[VendorResponse])
def get_vendors(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    try:
        vendors = db.query(Vendor).offset(skip).limit(limit).all()
        return vendors
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch vendors: {str(e)}"
        )


@router.get("/{vendor_id}", response_model=VendorResponse)
def get_vendor(vendor_id: int, db: Session = Depends(get_db)):
    try:
        vendor = db.query(Vendor).filter(Vendor.id == vendor_id).first()
        if not vendor:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Vendor with id {vendor_id} not found"
            )
        return vendor
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch vendor: {str(e)}"
        )


@router.post("/", response_model=VendorResponse, status_code=status.HTTP_201_CREATED)
def create_vendor(vendor: VendorCreate, db: Session = Depends(get_db)):
    try:
        db_vendor = Vendor(**vendor.model_dump())
        db.add(db_vendor)
        db.commit()
        db.refresh(db_vendor)
        return db_vendor
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create vendor: {str(e)}"
        )