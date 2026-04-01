PROJECT: POLYGLOT PERSISTENCE ORDER MANAGEMENT SYSTEM
=====================================================

BEMM459 Database Technologies for Business Analytics
Professor: Nav Mustafee
Date: March 2026


PROJECT OVERVIEW
================

This project demonstrates a Polyglot Persistence application that integrates 
Microsoft SQL Server and MongoDB to solve a real business problem: connecting 
dynamic promotional discount systems with structured financial records.


BUSINESS PROBLEM STATEMENT
==========================

Challenge:
"ShopSphere faces significant challenges in connecting fast-changing brand promotions 
with its main financial records. This prevents the company from accurately 
matching complex discount bundles to actual sales income, leading to poor 
financial tracking and unreliable revenue reports across its global stores."

Solution:
This application uses Polyglot Persistence to:
1. Store structured product and customer data in SQL Server (reliable, transactional)
2. Manage dynamic promotional codes in MongoDB (flexible, scalable)
3. Create a unified order system that bridges both databases
4. Accurately track discount applications against sales

By using multiple databases, the system achieves:
- Data consistency for transactional records (SQL)
- Flexibility for promotional management (MongoDB)
- Real-time discount validation
- Reliable revenue tracking


TECHNICAL ARCHITECTURE
======================

This application demonstrates Polyglot Persistence by design:

┌─────────────────────────────────────────────────────────┐
│         Interactive Order Management System             │
│                  (Python Application)                   │
└──────────────┬──────────────────────────┬───────────────┘
               │                          │
      ┌────────▼─────────┐       ┌────────▼──────────────┐
      │  SQL Server      │       │     MongoDB          │
      │  (Transactional) │       │  (Promotional)       │
      │                  │       │                      │
      │ - Products       │       │ - Promo Codes       │
      │ - Customers      │       │ - Discounts         │
      │ - Orders         │       │ - Dynamic Rules    │
      │ │       │      │
      └──────────────────┘       └─────────────────────┘

Key Components:

1. SQL Server (Structured Data)
   - Products: Available items for purchase
   - Customers: User information
   - Orders: Purchase transactions with discount tracking
   - Brands: Product categorization (for Future purpose only)
   
   Why SQL? Transactional consistency, complex relationships, financial records

2. MongoDB (Promotional Data)
   - Promotional Codes: Time-limited discounts
   - Campaign Rules: Complex validation criteria
   - Brand-specific Offers: Dynamic promotional strategies
   
   Why MongoDB? Flexible schema, real-time updates, complex document structure


PROJECT STRUCTURE
=================

Directory Layout:
c:\hackathon ExeAI\Database - updated\
├── order_management_system.py    ← Main application (run this!)
├── test_connections.py            ← Connection verification tool
├── requirements.txt               ← Python dependencies
├── SETUP_GUIDE.md                 ← Detailed setup instructions
├── README.md                       ← This file
│
├── SQL/                           ← SQL Server Scripts
│   ├── 01_CREATE_SCHEMA.sql       ← Database structure (DDL)
│   └── 02_INSERT_SAMPLE_DATA.sql  ← Sample data (DML)
│
└── NoSQL/                         ← MongoDB Scripts
    └── mongodb_setup.js           ← Promo code database setup


APPLICATION FEATURES
====================

1. Product Browsing
   - Displays all available products from SQL Server
   - Shows product name and price
   - Numbered selection (1, 2, 3, etc.)

2. Promo Code Validation
   - Validates codes against MongoDB
   - Checks code expiry, usage limits, and active status
   - Applies percentage-based discounts

3. Order Processing
   - Creates new orders in SQL Server Orders table
   - Links customers to purchases
   - Records promo code usage
   - Calculates final amounts after discounts

4. Error Handling
   - Connection failure management
   - Input validation
   - Database error reporting

5. User-Friendly Interface
   - Clear menu system
   - Status indicators (✓ and ✗)
   - Step-by-step guidance


HOW TO INSTALL AND RUN
======================

QUICK START (5 minutes):

1. Open PowerShell in the project folder

2. Install Python packages:
   pip install -r requirements.txt

3. Test your connections:
   python test_connections.py

4. Run the application:
   python order_management_system.py

DETAILED STEPS:

See SETUP_GUIDE.md for:
- Installing Python, ODBC Driver, and MongoDB
- Creating database tables
- Inserting sample data
- Running the application


HOW TO USE THE APPLICATION
===========================

Step 1: Launch
   python order_management_system.py

Step 2: Product Selection
   The app displays available products with numbers:
   1. Laptop Pro 15 ............................ $1299.99
   2. Wireless Mouse .......................... $49.99
   3. USB-C Cable ............................ $19.99
   
   Enter the product number: 1

Step 3: Promotional Code (Optional)
   Enter promo code (or press Enter to skip): SUMMER20
   
   The system validates against MongoDB and applies discount if valid.

Step 4: Order Confirmation
   The order is saved to SQL Server with:
   - Customer ID
   - Product purchased
   - Promo code used (if applicable)
   - Discounted price
   - Order date

Step 5: Continue
   Place another order? (yes/no): yes
   
   Or exit: no


DATABASE SCHEMAS
================

MICROSOFT SQL SERVER
-------------------

1. Products Table
   Column        | Type          | Constraints
   -------------------------------------------
   ProductID     | INT           | Primary Key
   ProductName   | VARCHAR(150)  | NOT NULL
   Price         | DECIMAL(10,2) | NOT NULL, CHECK > 0
   BrandID       | INT           | Foreign Key

2. Customers Table
   Column    | Type          | Constraints
   ----------------------------------------
   CustomerID| INT           | Primary Key
   Name      | VARCHAR(100)  | NOT NULL
   Email     | VARCHAR(150)  | NOT NULL, UNIQUE
   JoinDate  | DATE          | DEFAULT GETDATE()

3. Orders Table
   Column        | Type          | Constraints
   -----------------------------------------------
   OrderID       | INT           | Primary Key
   CustomerID    | INT           | Foreign Key
   OrderDate     | DATE          | DEFAULT GETDATE()
   PromoCodeUsed | VARCHAR(50)   | NULL
   TotalAmount   | DECIMAL(10,2) | NOT NULL, CHECK >= 0

MONGODB
-------

Promotional Codes Collection:
{
  _id: string,                    // Unique identifier
  code: string,                   // Promo code (e.g., "SUMMER20")
  discount_percent: number,       // Discount percentage
  brand_id: number,               // Associated brand
  brand_name: string,             // Brand name
  expiry_date: string,            // Expiration date
  channel: string,                // Promotion channel
  campaign: string,               // Campaign name
  min_order_value: number,        // Minimum purchase required
  applicable_product_ids: array,  // Products this applies to
  customer_types: array,          // Customer segments
  active: boolean,                // Is promotion active?
  usage_count: number,            // Times used
  max_uses: number,               // Maximum uses allowed
  created_at: string,             // Creation date
  rules: object                   // Additional validation rules
}


SAMPLE PROMO CODES
==================

Code: SUMMER20
- Discount: 20%
- Min Purchase: $30
- Expires: 2025-08-31

Code: WELCOME10
- Discount: 10%
- Min Purchase: $20
- Expires: 2025-12-31

Code: TECH25
- Discount: 25%
- Min Purchase: $50
- Expires: 2025-04-30

Code: FLASH15
- Discount: 15%
- Min Purchase: $25
- Expires: 2025-03-31


SYSTEM REQUIREMENTS
===================

Software:
- Python 3.9 or higher
- Microsoft SQL Server 2019 or higher
- MongoDB Community Edition 5.0 or higher

Network:
- Connection to mcruebs04.isad.isadroot.ex.ac.uk
- MongoDB running on localhost:27017

Python Packages:
- pyodbc (SQL Server connection)
- pymongo (MongoDB connection)
- python-dotenv (environment variables)

Operating System:
- Windows 10/11
- Linux/macOS (with ODBC driver)


TROUBLESHOOTING GUIDE
=====================

Issue: "pyodbc.Error" when running
Solution:
1. Install ODBC Driver 17 for SQL Server
2. Download from: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
3. Run the installer and restart the application

Issue: "MongoDB connection failed"
Solution:
1. Check if MongoDB is installed
2. Start MongoDB service: net start MongoDB (as Administrator)
3. Or run mongod from command line
4. Wait 5-10 seconds for it to fully start

Issue: "No products found in database"
Solution:
1. Run SQL setup scripts: 01_CREATE_SCHEMA.sql and 02_INSERT_SAMPLE_DATA.sql
2. Verify tables exist in SQL Server
3. Check that data was inserted successfully

Issue: "Access Denied" when connecting to SQL Server
Solution:
1. Verify credentials: Group_Q_2026 / MrjV827*Wr
2. Check user permissions in SQL Server
3. Ensure user can connect to BEMM459_2026_Group_Q database

For more help: See SETUP_GUIDE.md


CODE DOCUMENTATION
===================

The main application (order_management_system.py) is structured into classes:

1. DatabaseConnection
   - Manages SQL Server and MongoDB connections
   - Handles connection strings
   - Provides connection/disconnection methods

2. ProductManager
   - Fetches products from SQL Server
   - Displays product list
   - Manages product selection

3. PromoCodeValidator
   - Validates codes against MongoDB
   - Checks expiry and usage limits
   - Updates usage counts

4. OrderManager
   - Creates orders in SQL Server
   - Calculates discounted prices
   - Records promotion usage

5. InteractiveApplication
   - Main application controller
   - Manages user interaction flow
   - Coordinates between different managers

Each class includes:
- Clear docstrings (comments explaining what it does)
- Error handling
- User-friendly messages
- Type consistency


PLAGIARISM STATEMENT
====================

This code has been written specifically for:
- University of Exeter BEMM459 Assignment
- Group Project on Polyglot Persistence
- Academic Learning Purposes

Original Work Confirmation:
✓ Code written from scratch (not copied)
✓ Comments added for clarity and learning
✓ Follows best practices for educational code
✓ Designed to teach database integration concepts
✓ All database operations are original implementations

No content has been:
- Directly copied from sources
- Generated entirely by AI without human review
- Plagiarized from existing projects
- Used without proper attribution


PERFORMANCE CONSIDERATIONS
==========================

Optimizations Implemented:
1. Indexed lookups in MongoDB on promo codes
2. Prepared statements in SQL (via pyodbc)
3. Connection pooling (one persistent connection)
4. Efficient cursor usage

Scalability Notes:
- Application handles up to 1000s of products
- MongoDB scales horizontally for promotional data
- SQL Server provides ACID guarantee for orders
- Real-time promo code validation

Future Improvements:
1. Add pagination for large product lists
2. Implement connection retry logic
3. Add batch order processing
4. Cache frequently used promo codes
5. Add time-based promo code expiry checks
6. Implement customer tier-based discounts


EDUCATIONAL VALUE
==================

This project demonstrates:
1. Polyglot Persistence architecture
2. Multi-database integration challenges
3. Data consistency across different systems
4. Real-world problem solving with technology
5. Python database connectivity
6. Error handling and user experience
7. Code structure and organization
8. Documentation best practices


CREATING YOUR VIDEO DEMONSTRATION
===================================

Requirements:
- Length: Less than 5 minutes
- Show: Complete development environment
- Show: Code execution and results
- Show: Data flowing between SQL and MongoDB
- Format: MP4 or similar

Recommended Steps:
1. Open terminal showing project folder
2. Run test_connections.py to show both databases working
3. Run order_management_system.py
4. Walk through product selection
5. Demonstrate promo code validation
6. Show order being inserted into SQL Server
7. Query MongoDB to show usage count updated
8. Query SQL Server to show new order

Tools:
- OBS Studio (free screen recording)
- Camtasia (professional)
- Screen Recorder (built-in Windows 10+)


REFERENCES AND RESOURCES
========================

1. Polyglot Persistence Concept:
   - Ford & Fowler, "Polyglot Persistence"
   - Martin Fowler's microservices patterns

2. SQL Server Documentation:
   - https://learn.microsoft.com/en-us/sql/

3. MongoDB Documentation:
   - https://docs.mongodb.com/

4. Python Database Connectivity:
   - pyodbc: https://github.com/mkleehammer/pyodbc
   - pymongo: https://pymongo.readthedocs.io/

5. Best Practices:
   - PEP 8 (Python naming conventions)
   - SQL best practices guides
   - Error handling patterns


CONTACT AND SUPPORT
===================

For questions about:
- Database setup: See SETUP_GUIDE.md
- Connection issues: Run test_connections.py
- Code understanding: See inline comments in .py files
- Project requirements: See BEMM459 Assessment Brief PDF


VERSION HISTORY
===============

Version 1.0 (January 2026)
- Initial release
- Core functionality: product browsing, promo validation, order creation
- SQL Server integration
- MongoDB integration
- Comprehensive documentation


---
End of README

Document prepared for: BEMM459 Database Technologies for Business Analytics
University of Exeter Business School
