"""
Optional seed script — populates the DB with sample vendors, products, and a PO.
Run once after the server has started (tables must already exist):
    python seed.py
"""
from database import SessionLocal
from models import Vendor, Product, PurchaseOrder, PurchaseOrderItem, POStatus
from routes.po_routes import calculate_total


def seed():
    db = SessionLocal()
    try:
        # ── Vendors ────────────────────────────────────────────────────────
        vendors = [
            Vendor(name="Acme Supplies", contact="acme@example.com", rating=4.5),
            Vendor(name="Global Parts Co.", contact="global@example.com", rating=3.8),
        ]
        db.add_all(vendors)
        db.flush()

        # ── Products ───────────────────────────────────────────────────────
        products = [
            Product(name="Laptop", sku="SKU-001", unit_price=999.99, stock_level=50),
            Product(name="Wireless Mouse", sku="SKU-002", unit_price=29.99, stock_level=200),
            Product(name="USB-C Hub", sku="SKU-003", unit_price=49.99, stock_level=150),
        ]
        db.add_all(products)
        db.flush()

        # ── Purchase Order ─────────────────────────────────────────────────
        po = PurchaseOrder(
            reference_no="PO-2024-0001",
            vendor_id=vendors[0].id,
            status=POStatus.SUBMITTED,
            total_amount=0.0
        )
        db.add(po)
        db.flush()

        items = [
            PurchaseOrderItem(po_id=po.id, product_id=products[0].id, quantity=2, price=999.99),
            PurchaseOrderItem(po_id=po.id, product_id=products[1].id, quantity=5, price=29.99),
        ]
        db.add_all(items)
        db.flush()

        po.total_amount = calculate_total(items)

        db.commit()
        print("✅ Seed data inserted successfully.")
        print(f" PO total (with 5% tax): ${po.total_amount}")

    except Exception as e:
        db.rollback()
        print(f"❌ Seeding failed: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    seed()