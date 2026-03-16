BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "products" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(255) NOT NULL,
	"sku"	VARCHAR(100) NOT NULL,
	"unit_price"	FLOAT NOT NULL,
	"stock_level"	INTEGER,
	PRIMARY KEY("id"),
	UNIQUE("sku")
);
CREATE TABLE IF NOT EXISTS "purchase_order_items" (
	"id"	INTEGER NOT NULL,
	"po_id"	INTEGER NOT NULL,
	"product_id"	INTEGER NOT NULL,
	"quantity"	INTEGER NOT NULL,
	"price"	FLOAT NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("po_id") REFERENCES "purchase_orders"("id"),
	FOREIGN KEY("product_id") REFERENCES "products"("id")
);
CREATE TABLE IF NOT EXISTS "purchase_orders" (
	"id"	INTEGER NOT NULL,
	"reference_no"	VARCHAR(100) NOT NULL,
	"vendor_id"	INTEGER NOT NULL,
	"total_amount"	FLOAT,
	"status"	VARCHAR(9),
	PRIMARY KEY("id"),
	UNIQUE("reference_no"),
	FOREIGN KEY("vendor_id") REFERENCES "vendors"("id")
);
CREATE TABLE IF NOT EXISTS "vendors" (
	"id"	INTEGER NOT NULL,
	"name"	VARCHAR(255) NOT NULL,
	"contact"	VARCHAR(255) NOT NULL,
	"rating"	FLOAT,
	PRIMARY KEY("id")
);
INSERT INTO "products" VALUES (1,'Laptop','SKU-001',999.99,50);
INSERT INTO "products" VALUES (2,'Wireless Mouse','SKU-002',29.99,200);
INSERT INTO "products" VALUES (3,'USB-C Hub','SKU-003',49.99,150);
INSERT INTO "products" VALUES (4,'Laptop','LP100',800.0,20);
INSERT INTO "purchase_order_items" VALUES (1,1,1,2,999.99);
INSERT INTO "purchase_order_items" VALUES (2,1,2,5,29.99);
INSERT INTO "purchase_orders" VALUES (1,'PO-2024-0001',1,2257.43,'SUBMITTED');
INSERT INTO "vendors" VALUES (1,'Acme Supplies','acme@example.com',4.5);
INSERT INTO "vendors" VALUES (2,'Global Parts Co.','global@example.com',3.8);
INSERT INTO "vendors" VALUES (3,'ABC Supplier','abc@supplier.com',4.0);
INSERT INTO "vendors" VALUES (4,'ABC Supplier','abc@supplier.com',4.0);
CREATE INDEX IF NOT EXISTS "ix_products_id" ON "products" (
	"id"
);
CREATE INDEX IF NOT EXISTS "ix_purchase_order_items_id" ON "purchase_order_items" (
	"id"
);
CREATE INDEX IF NOT EXISTS "ix_purchase_orders_id" ON "purchase_orders" (
	"id"
);
CREATE INDEX IF NOT EXISTS "ix_vendors_id" ON "vendors" (
	"id"
);
COMMIT;
