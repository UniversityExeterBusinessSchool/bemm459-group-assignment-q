|  |
| --- |
| **POLYGLOT PERSISTENCE** |
| Order Management System |
| *Integrating Microsoft SQL Server & MongoDB for Dynamic Discount Management* |

|  |  |
| --- | --- |
| **Module** | BEMM459 — Database Technologies for Business Analytics |
| **Supervisor** | Professor Nav Mustafee |
| **Institution** | University of Exeter Business School |
| **Submission** |28th March 2026 |
| **Version** | 1.0 — Initial Release |

**ABSTRACT**
============

This document provides comprehensive technical and operational documentation for the Polyglot Persistence Order Management System, developed as part of the BEMM459 Database Technologies for Business Analytics group project. The system addresses a real-world business challenge faced by the fictional retail enterprise ShopSphere: the inability to reconcile dynamic promotional campaigns with structured financial transaction records. By adopting a polyglot persistence architecture — combining Microsoft SQL Server for transactional integrity and MongoDB for flexible promotional data management — this project demonstrates how heterogeneous database systems can be unified within a single Python-based application to deliver accurate, real-time discount validation and revenue tracking.

**1. BUSINESS PROBLEM STATEMENT**
=================================

ShopSphere is a global retail organisation operating across multiple territories, each with independently managed promotional campaigns and a centralised financial reporting infrastructure. The core business challenge can be articulated as follows:

|  |  |
| --- | --- |
|  | *"ShopSphere faces significant challenges in connecting fast-changing brand promotions with its main financial records. This prevents the company from accurately matching complex discount bundles to actual sales income, leading to poor financial tracking and unreliable revenue reports across its global stores."* |

This project addresses three primary failure points identified in the current system:

* Promotional discount data is stored in rigid relational schemas ill-suited to frequent structural changes.
* There is no real-time validation mechanism to ensure that discount codes are applied within their eligibility constraints.
* Revenue reports cannot reliably reconcile applied discounts against actual transaction records.

**2. PROPOSED SOLUTION**
========================

The system resolves the above challenges through a polyglot persistence strategy, whereby data is stored in the database engine best suited to its structural and operational characteristics:

|  |  |
| --- | --- |
| **Microsoft SQL Server**  *Transactional & Structured Data* | **MongoDB**  *Promotional & Document Data* |
| * Products, Customers, Orders * ACID-compliant transactions * Complex relational queries * Authoritative financial records | * Promotional codes & campaigns * Flexible document schema * Real-time rule validation * Horizontal scalability |

**3. TECHNICAL ARCHITECTURE**
=============================

The application follows a three-tier architecture in which the Python layer acts as the integration bridge between the two independently managed database systems. The core design principle is separation of concerns: each database is responsible solely for the data type for which it is architecturally optimised.

|  |
| --- |
| ┌─────────────────────────────────────────────────────────────────┐ |
| │ Interactive Order Management Application │ |
| │ (Python — CLI Interface) │ |
| └────────────────┬────────────────────────────┬───────────────────┘ |
| │ │ |
| ┌──────────▼──────────┐ ┌─────────▼──────────────────┐ |
| │ SQL Server │ │ MongoDB │ |
| │ (Transactional) │ │ (Promotional) │ |
| │ │ │ │ |
| │ ▸ Products │ │ ▸ Promo Codes │ |
| │ ▸ Customers │ │ ▸ Campaign Rules │ |
| │ ▸ Orders │ │ ▸ Brand-Specific Offers │ |
| │ ▸ Brands (future) │ │ ▸ Usage Tracking │ |
| └─────────────────────┘ └────────────────────────────┘ |

**3.1 Class Structure**
-----------------------

The Python application is architected around five distinct manager classes, each encapsulating a single domain of responsibility:

|  |  |
| --- | --- |
| **Class** | **Responsibility** |
| DatabaseConnection | Manages connection lifecycles for both SQL Server and MongoDB. |
| ProductManager | Fetches and presents product listings from SQL Server. |
| PromoCodeValidator | Validates promotional codes against MongoDB rules and constraints. |
| OrderManager | Persists order records and discount applications to SQL Server. |
| InteractiveApplication | Orchestrates user interaction and coordinates between managers. |

**4. PROJECT STRUCTURE**
========================

|  |
| --- |
| project-root/ |
| ├── order\_management\_system.py ← Main application entry point |
| ├── test\_connections.py ← Database connection verification |
| ├── requirements.txt ← Python package dependencies |
| ├── SETUP\_GUIDE.md ← Environment setup instructions |
| ├── README.md ← This document |
| │ |
| ├── SQL/ |
| │ ├── 01\_CREATE\_SCHEMA.sql ← DDL — Database schema definition |
| │ └── 02\_INSERT\_SAMPLE\_DATA.sql ← DML — Sample seed data |
| │ |
| └── NoSQL/ |
| └── mongodb\_setup.js ← MongoDB collection & document initialisation |

**5. DATABASE SCHEMAS**
=======================

**5.1 Microsoft SQL Server**
----------------------------

**Products Table**

|  |  |  |
| --- | --- | --- |
| **Column** | **Type** | **Constraints** |
| ProductID | INT | PRIMARY KEY, IDENTITY |
| ProductName | VARCHAR(150) | NOT NULL |
| Price | DECIMAL(10,2) | NOT NULL, CHECK (Price > 0) |
| BrandID | INT | FOREIGN KEY → Brands(BrandID) |

**Customers Table**

|  |  |  |
| --- | --- | --- |
| **Column** | **Type** | **Constraints** |
| CustomerID | INT | PRIMARY KEY, IDENTITY |
| Name | VARCHAR(100) | NOT NULL |
| Email | VARCHAR(150) | NOT NULL, UNIQUE |
| JoinDate | DATE | DEFAULT GETDATE() |

**Orders Table**

|  |  |  |
| --- | --- | --- |
| **Column** | **Type** | **Constraints** |
| OrderID | INT | PRIMARY KEY, IDENTITY |
| CustomerID | INT | FOREIGN KEY → Customers(CustomerID) |
| OrderDate | DATE | DEFAULT GETDATE() |
| PromoCodeUsed | VARCHAR(50) | NULL |
| TotalAmount | DECIMAL(10,2) | NOT NULL, CHECK (TotalAmount >= 0) |

**5.2 MongoDB — Promotional Codes Collection**
----------------------------------------------

|  |
| --- |
| { |
| "\_id" : String, // Unique document identifier |
| "code" : String, // Promotional code (e.g. "SUMMER20") |
| "discount\_percent" : Number, // Percentage discount applied |
| "brand\_id" : Number, // Associated brand identifier |
| "brand\_name" : String, // Human-readable brand label |
| "expiry\_date" : String, // ISO 8601 expiry date |
| "channel" : String, // Distribution channel (e.g. "online") |
| "campaign" : String, // Campaign name |
| "min\_order\_value" : Number, // Minimum qualifying purchase amount |
| "applicable\_product\_ids": Array, // Eligible product IDs |
| "customer\_types" : Array, // Target customer segments |
| "active" : Boolean, // Whether the code is currently active |
| "usage\_count" : Number, // Number of times used |
| "max\_uses" : Number, // Maximum permitted uses |
| "created\_at" : String, // Document creation timestamp |
| "rules" : Object // Additional validation rules |
| } |

**6. SAMPLE PROMOTIONAL CODES**
===============================

The following promotional codes are pre-loaded into the MongoDB collection for demonstration and testing purposes:

|  |  |  |  |
| --- | --- | --- | --- |
| **Code** | **Discount** | **Min. Purchase** | **Expiry Date** |
| SUMMER20 | 20% | $30.00 | 31 August 2025 |
| WELCOME10 | 10% | $20.00 | 31 December 2025 |
| TECH25 | 25% | $50.00 | 30 April 2025 |
| FLASH15 | 15% | $25.00 | 31 March 2025 |

**7. INSTALLATION & SETUP**
===========================

**7.1 System Requirements**
---------------------------

|  |  |
| --- | --- |
| **Component** | **Minimum Version** |
| Python | 3.9 or higher |
| Microsoft SQL Server | 2019 or higher |
| MongoDB Community Edition | 5.0 or higher |
| ODBC Driver for SQL Server | Version 17 |

**Required Python packages (see requirements.txt):**

* pyodbc — SQL Server connectivity via ODBC
* pymongo — MongoDB driver for Python
* python-dotenv — Environment variable management

**7.2 Quick Start**
-------------------

Execute the following commands in sequence from the project root directory:

|  |
| --- |
| # Step 1 — Install Python dependencies |
| pip install -r requirements.txt |
|  |
| # Step 2 — Verify database connectivity |
| python test\_connections.py |
|  |
| # Step 3 — Launch the application |
| python order\_management\_system.py |

For a full environment configuration walkthrough — including SQL Server schema creation, sample data insertion, and MongoDB initialisation — refer to SETUP\_GUIDE.md.

**8. APPLICATION WORKFLOW**
===========================

The application presents an interactive command-line interface that guides the user through the following workflow:

1. Launch the application via python order\_management\_system.py.
2. Browse the product catalogue retrieved dynamically from SQL Server.
3. Select a product by its displayed index number.
4. Optionally, enter a promotional code for real-time validation against MongoDB.
5. Confirm the order; the system calculates the discounted total and persists the transaction to SQL Server.
6. Choose to place a further order or exit the application.

**9. TROUBLESHOOTING**
======================

|  |  |  |
| --- | --- | --- |
| **Error** | **Cause** | **Resolution** |
| pyodbc.Error on startup | ODBC Driver 17 not installed | Download and install from Microsoft's official documentation site. |
| MongoDB connection failed | MongoDB service not running | Run net start MongoDB as Administrator, or execute mongod from the terminal. |
| No products found | SQL schema/data not initialised | Execute 01\_CREATE\_SCHEMA.sql and 02\_INSERT\_SAMPLE\_DATA.sql in SQL Server. |
| Access Denied (SQL Server) | Invalid credentials or permissions | Verify username, password, and database access for BEMM459\_2026\_Group\_Q. |

**10. PERFORMANCE CONSIDERATIONS & FUTURE WORK**
================================================

**10.1 Current Optimisations**
------------------------------

* Indexed lookups on promotional code fields in MongoDB.
* Parameterised SQL statements via pyodbc, preventing SQL injection and improving query plan reuse.
* Persistent connection pooling — a single connection per database is maintained throughout the session.
* Efficient cursor management to minimise memory overhead.

**10.2 Proposed Enhancements**
------------------------------

* Pagination for large product catalogues.
* Automatic connection retry logic with exponential back-off.
* Batch order processing for high-throughput scenarios.
* Server-side caching of frequently validated promotional codes.
* Time-zone-aware expiry checking for global campaign management.
* Customer tier-based discount stratification.

**11. LEARNING OUTCOMES DEMONSTRATED**
======================================

This project serves as a practical illustration of the following academic and professional competencies:

* Polyglot persistence architectural design and rationale.
* Integration of heterogeneous database systems within a single application.
* Trade-off analysis between relational (ACID) and document (BASE) models.
* Python database connectivity using industry-standard drivers.
* Robust error handling and graceful degradation strategies.
* Modular, object-oriented code design following PEP 8 conventions.
* Comprehensive technical documentation to professional standards.

**12. REFERENCES**
==================

Ford, N. & Fowler, M. (2012). Polyglot Persistence. O'Reilly Media.

Fowler, M. (2014). Microservices Patterns. martinfowler.com.

Microsoft (2024). SQL Server 2019 Documentation. https://learn.microsoft.com/en-us/sql/

MongoDB Inc. (2024). MongoDB 5.0 Manual. https://docs.mongodb.com/

mkleehammer (2024). pyodbc — Python ODBC Library. https://github.com/mkleehammer/pyodbc

MongoDB Inc. (2024). PyMongo Documentation. https://pymongo.readthedocs.io/

Python Software Foundation (2023). PEP 8 — Style Guide for Python Code. https://peps.python.org/pep-0008/

**ACADEMIC INTEGRITY STATEMENT**
================================

This project has been produced in its entirety by the members of Group Q as an original academic submission for BEMM459 Database Technologies for Business Analytics at the University of Exeter Business School. All code, documentation, and design decisions are the product of independent group effort. Where external resources have informed the work, they are appropriately cited in Section 12. The group confirms that:

* No source code has been directly copied from external repositories without attribution.
* All database operations are original implementations.
* Documentation has been authored specifically for this submission.
* AI-assisted tools, where employed, were used only to support — not replace — original thinking, and all outputs were reviewed and substantially revised by group members.

*BEMM459 Group Q · University of Exeter Business School · March 2026*