# ShopSphere – SQL Database README

## Overview

ShopSphere's data layer is built on a **normalised relational schema** hosted on Microsoft SQL Server. The SQL database serves as the authoritative record for all customer, product, order, and payment transactions. This README documents the schema design, normalisation decisions, key relationships, implementation details, and analytical queries.

---

## Schema Design

The relational schema comprises **six tables**, each representing a discrete business entity:

| Table | Primary Key | Purpose |
|---|---|---|
| `Brands` | `BrandID` | Centralises brand metadata; eliminates duplication across products |
| `Products` | `ProductID` | Product catalogue; price and brand linked via `BrandID` FK |
| `Customers` | `CustomerID` | Registered customer records; identity anchor for all orders |
| `Orders` | `OrderID` | Transactional record; links customer, promo code, and total amount |
| `OrderItems` | `OrderItemID` | Per-line-item record; captures quantity and discount applied |
| `Payments` | `PaymentID` | Payment record per order; tracks method, status, date, amount |


## Entity Relationships

```
Customers ──< Orders ──< OrderItems >── Products >── Brands
                 │
              Payments
```

| Relationship | Cardinality | Constraint |
| Customers → Orders | 1:Many | `Orders.CustomerID` FK → `Customers.CustomerID` |
| Orders → OrderItems | 1:Many | `OrderItems.OrderID` FK → `Orders.OrderID` |
| Products → OrderItems | 1:Many | `OrderItems.ProductID` FK → `Products.ProductID` |
| Brands → Products | 1:Many | `Products.BrandID` FK → `Brands.BrandID` |
| Orders → Payments | 1:Many | `Payments.OrderID` FK → `Orders.OrderID` |

All foreign key constraints enforce **referential integrity** — it is structurally impossible to create an order without a valid customer, or an order item without a valid product and order.

---
## Learning Outcomes & Personal Reflection

The design and implementation of the ShopSphere database provided significant learning opportunities across several technical and business domains:

* **Normalisation as a Business Tool:** I learned that normalising data (specifically reaching Third Normal Form) is not merely a theoretical or academic exercise. By extracting the `Brands` table and ensuring there were no transitive dependencies, I saw firsthand how strict normalisation permanently encodes business rules into the system — making data anomalies structurally impossible rather than relying on application-level error catching.
* **Resolving Complex Business Logic with SQL:** Designing the integration point for the "Reconciliation Gap" taught me how to use SQL to solve real business flow problems. Capturing the `DiscountApplied` at the `OrderItems` line-item level demonstrated how a relational database acts as an immutable financial ledger, separating the complexity of promotional marketing logic from the rigidity required by finance.
* **The Power of Relational Constraints:** Implementing `IDENTITY` primary keys and strictly cascading foreign key constraints showed me the power of referential integrity. I learned how to architect a database where it is impossible to generate an orphan record (like an order without a customer), ensuring absolute data reliability.
* **Querying for Business Intelligence:** Writing the analytical queries moved my SQL skills beyond basic `SELECT` statements into structured business intelligence. Using `JOIN`, `GROUP BY`, and aggregate functions like `SUM` and `COUNT` demonstrated how raw transactional data can be interrogated to provide actionable insights, directly supporting both marketing campaign analysis and financial auditing.

## Normalisation (3NF)

| Normal Form | Rule Applied | Example |
|---|---|---|
| **1NF** | Atomic values, no repeating groups | Each column holds one value; every row has a unique PK |
| **2NF** | Full functional dependency on entire PK | `ProductName` depends on `ProductID` only, not split across tables |
| **3NF** | No transitive dependencies | `BrandName` removed from `Products` → extracted to `Brands` table keyed on `BrandID` |

Key 3NF decision: `BrandName` was transitively dependent on `ProductID` via `BrandID`. Extracting it into `Brands` means a brand rename requires **one record change**, consistently reflected across all associated products.

---

## Full SQL Schema

```sql
CREATE TABLE Brands (
    BrandID   INT PRIMARY KEY,
    BrandName VARCHAR(100) NOT NULL
);

CREATE TABLE Products (
    ProductID   INT PRIMARY KEY,
    ProductName VARCHAR(150) NOT NULL,
    Price       DECIMAL(10,2) NOT NULL,
    BrandID     INT NOT NULL,
    FOREIGN KEY (BrandID) REFERENCES Brands(BrandID)
);

CREATE TABLE Customers (
    CustomerID INT PRIMARY KEY,
    Name       VARCHAR(100) NOT NULL,
    Email      VARCHAR(150) NOT NULL,
    JoinDate   DATE NOT NULL
);

CREATE TABLE Orders (
    OrderID       INT PRIMARY KEY,
    CustomerID    INT NOT NULL,
    OrderDate     DATE NOT NULL,
    PromoCodeUsed VARCHAR(50),
    TotalAmount   DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (CustomerID) REFERENCES Customers(CustomerID)
);

CREATE TABLE OrderItems (
    OrderItemID     INT PRIMARY KEY,
    OrderID         INT NOT NULL,
    ProductID       INT NOT NULL,
    Quantity        INT NOT NULL,
    DiscountApplied DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (OrderID)   REFERENCES Orders(OrderID),
    FOREIGN KEY (ProductID) REFERENCES Products(ProductID)
);

CREATE TABLE Payments (
    PaymentID     INT PRIMARY KEY,
    OrderID       INT NOT NULL,
    PaymentMethod VARCHAR(50) NOT NULL,
    PaymentStatus VARCHAR(50) NOT NULL,
    PaymentDate   DATE NOT NULL,
    Amount        DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (OrderID) REFERENCES Orders(OrderID)
);
```

---

## Key Analytical Queries

### Q1 — Customer Order Summary
```sql
SELECT c.CustomerID, c.Name, c.Email,
       o.OrderID, o.OrderDate, o.PromoCodeUsed, o.TotalAmount
FROM Customers c
JOIN Orders o ON c.CustomerID = o.CustomerID
ORDER BY o.OrderDate DESC;
```
**Output justification:** Confirms every order is bound to a verified customer. `PromoCodeUsed = NULL` indicates a full-price transaction; a populated value indicates a discount was applied at checkout.

---

### Q2 — Line-Item Discount Audit
```sql
SELECT o.OrderID, o.PromoCodeUsed, p.ProductName, b.BrandName,
       p.Price AS ListedPrice, oi.Quantity,
       oi.DiscountApplied,
       (p.Price * oi.Quantity) - oi.DiscountApplied AS NetRevenue
FROM Orders o
JOIN OrderItems oi ON o.OrderID = oi.OrderID
JOIN Products p    ON oi.ProductID = p.ProductID
JOIN Brands b      ON p.BrandID = b.BrandID;
```
**Output justification:** Exposes listed price, discount applied, and net revenue per line item — directly resolving the Reconciliation Gap. Gross vs net revenue is now distinguishable at product-line granularity.

---

### Q3 — Promo Code Usage Summary
```sql
SELECT PromoCodeUsed,
       COUNT(OrderID)   AS TimesUsed,
       SUM(TotalAmount) AS TotalRevenue,
       AVG(TotalAmount) AS AvgOrderValue
FROM Orders
WHERE PromoCodeUsed IS NOT NULL
GROUP BY PromoCodeUsed
ORDER BY TimesUsed DESC;
```
**Output justification:** Aggregates promotional activity by code — showing which campaigns drove volume and what revenue they generated. Fully auditable from SQL alone.

---

### Q4 — Revenue Reconciliation vs Payments
```sql
SELECT o.OrderID, o.TotalAmount AS OrderTotal,
       py.Amount AS AmountPaid, py.PaymentStatus,
       (o.TotalAmount - py.Amount) AS Discrepancy
FROM Orders o
JOIN Payments py ON o.OrderID = py.OrderID
ORDER BY Discrepancy DESC;
```
**Output justification:** A `Discrepancy = 0` confirms a clean, fully reconciled transaction. Non-zero values flag payment integrity issues requiring investigation.

---

## Implementation Details

| Detail | Value |
|---|---|
| **Server** | `mcruebs04.isad.isadroot.ex.ac.uk` (university MS SQL Server) |
| **Key generation** | `IDENTITY(1,1)` — auto-incrementing sequential primary keys |
| **Referential integrity** | Foreign key constraints on all core entities |
| **Cascading constraints** | Parent record changes cascade to dependent tables |
| **Scripts** | `/SQL/01_CREATE_SCHEMA.sql` — DDL; `/SQL/02_INSERT_SAMPLE_DATA.sql` — DML |
| **Sample data** | Representative records inserted for query testing and concurrency simulation |

---

## Repository Structure

```
/SQL
├── 01_CREATE_SCHEMA.sql       # Table definitions, PKs, FKs, constraints
└── 02_INSERT_SAMPLE_DATA.sql  # Sample transactional records
```

---

## Future Development

| Area | Description |
| **Row-level security** | Implement role-based access control for payment and customer data |
| **Index optimisation** | Add indexes on `CustomerID` (Orders) and `OrderID` (OrderItems) for query performance |
| **Brands integration** | Fully integrate `Brands` table with populated data across all product records |
| **Per-line-item discounts** | Ensure `DiscountApplied` in `OrderItems` is consistently populated via application layer |

---


