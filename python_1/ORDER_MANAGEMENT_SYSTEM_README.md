# Order Management System - Complete Documentation
## Polyglot Persistence Application (SQL Server + MongoDB)

---

## 📋 TABLE OF CONTENTS
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Class Overview](#class-overview)
4. [Usage Scenarios](#usage-scenarios)
5. [Database Connections](#database-connections)
6. [Customer Management](#customer-management)
7. [Product Management](#product-management)
8. [Promo Code Validation](#promo-code-validation)
9. [Order Processing](#order-processing)
10. [Error Handling](#error-handling)
11. [Configuration](#configuration)
12. [Running the Application](#running-the-application)

---

## 📖 OVERVIEW

The **Order Management System** is a polyglot persistence application that demonstrates integration between:
- **SQL Server**: Manages structured, transactional data (customers, orders)
- **MongoDB**: Manages flexible, dynamic data (promotional codes)

This application shows how modern systems can use multiple databases simultaneously, each optimized for specific data characteristics.

### Key Purpose
- Display products from SQL Server
- Validate promotional codes from MongoDB
- Process customer orders with discount calculation
- Persist order data across both database systems

---

## 🏗️ SYSTEM ARCHITECTURE

```
┌──────────────────────────────────────────────┐
│   InteractiveApplication (Main Controller)   │
│                                              │
│  - Manages user interaction flow             │
│  - Coordinates between managers              │
│  - Handles customer registration            │
│  - Processes order workflow                 │
└────────────┬─────────────────────────────────┘
             │
    ┌────────┼────────┐
    │        │        │
    ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐
│ Prod │ │Promo │ │Order │
│ Mgmt │ │Valid │ │Mgmt  │
└───┬──┘ └───┬──┘ └───┬──┘
    │        │        │
    └────────┼────────┘
             │
             ▼
   ┌─────────────────────┐
   │ DatabaseConnection  │
   │                     │
   │  SQL Server         │
   │  MongoDB            │
   └─────────────────────┘
```

---

## 📦 CLASS OVERVIEW

### 1. **DatabaseConnection**
**Purpose**: Manages all database connections and operations

**Responsibilities**:
- Establish SQL Server connection (with ODBC driver fallback)
- Establish MongoDB connection
- Customer lookup by email
- Customer creation/registration
- Customer order count queries
- Connection cleanup

**Key Methods**:
- `connect_sql_server()` - Connect with SSL encryption
- `connect_mongodb()` - Connect to MongoDB
- `get_customer_id_by_email(email)` - Look up existing customer
- `get_customer_order_count(customer_id)` - Count customer's orders
- `insert_customer(email, name)` - Create new customer
- `disconnect()` - Close all connections

---

### 2. **ProductManager**
**Purpose**: Handles product-related operations

**Responsibilities**:
- Fetch products from SQL Server
- Store product data in memory
- Display products with pricing
- Fallback to sample data if database unavailable

**Key Methods**:
- `fetch_all_products()` - Retrieve all products from SQL Server
- `display_products()` - Show formatted product list with prices

---

### 3. **PromoCodeValidator**
**Purpose**: Validates promotional codes using MongoDB

**Responsibilities**:
- Check promo code existence
- Validate code activation status
- Check usage limits
- Verify minimum order amounts
- Enforce first-order-only restrictions
- Update usage counts

**Key Methods**:
- `validate_promo_code(code, order_value, customer_id)` - Comprehensive validation
- `update_usage_count(promo_code)` - Increment usage counter

---

### 4. **OrderManager**
**Purpose**: Creates and manages orders

**Responsibilities**:
- Generate unique order IDs
- Calculate discounts
- Create order records in SQL Server
- Store complete order details

**Key Methods**:
- `create_order(customer_id, product_id, product_price, promo_code, discount_percent)` - Process complete order

---

### 5. **InteractiveApplication**
**Purpose**: Main application controller and user interface

**Responsibilities**:
- Initialize all managers and connections
- Handle user interaction flow
- Manage customer authentication/registration
- Process order workflow
- Handle application lifecycle

**Key Methods**:
- `initialize()` - Setup connections and managers
- `get_customer_email()` - Authenticate or register customer
- `display_products()` - Show available products
- `get_product_selection()` - Get user's product choice
- `get_promo_code()` - Get user's promo code (optional)
- `process_order()` - Execute complete order workflow
- `run()` - Main application loop

---

## 🎯 USAGE SCENARIOS

### **Scenario 1: First-Time Customer Purchasing**

**Flow**:
1. User enters email address
2. System checks if customer exists in SQL Server
3. Customer NOT found → System prompts for name
4. New customer account created in SQL Server
5. User browses products
6. User selects product and applies promo code
7. Promo code validated against MongoDB
8. Order created and saved to SQL Server

**Database Operations**:
- SQL Server: INSERT new Customer record
- SQL Server: SELECT Products
- MongoDB: FIND promo code + validate
- MongoDB: UPDATE usage count
- SQL Server: INSERT Order record

---

### **Scenario 2: Returning Customer Purchasing**

**Flow**:
1. User enters email address
2. System finds existing customer in SQL Server
3. Welcome back message displayed
4. User browsed products from SQL Server (or sample)
5. User selects product
6. Optional promo code applied
7. Promo validation considers customer's order history
8. Order created with discount (if applicable)

**Database Operations**:
- SQL Server: SELECT Customer by email
- SQL Server: SELECT Products
- SQL Server: COUNT customer's previous orders
- MongoDB: FIND and VALIDATE promo code
- MongoDB: UPDATE usage count
- SQL Server: INSERT Order with discount

---

### **Scenario 3: Invalid Promo Code Application**

**Flow**:
1. User selects product ($50)
2. User enters invalid/non-existent promo code
3. System queries MongoDB for code
4. Code NOT found in database
5. System rejects code with error message
6. User proceeds without discount
7. Order created at full price

**Database Operations**:
- MongoDB: FIND returns NULL
- SQL Server: INSERT Order with 0 discount

---

### **Scenario 4: Promo Code with Usage Limit Exceeded**

**Flow**:
1. User selects product
2. User enters valid promo code (e.g., "SUMMER20")
3. System validates:
   - Code exists ✓
   - Code is active ✓
   - Usage count (100) >= Maximum uses (100) ✗
4. System rejects: "Code has reached maximum uses"
5. Order proceeds without discount

**Database Operations**:
- MongoDB: FIND promo code, check usage_count vs max_uses
- SQL Server: INSERT Order with 0 discount

---

### **Scenario 5: Promo Code with Minimum Order Amount**

**Flow**:
1. User selects product ($20)
2. User enters promo code (requires minimum $50)
3. System validates:
   - Code exists ✓
   - Code is active ✓
   - Usage limit not reached ✓
   - Order value ($20) < Minimum ($50) ✗
4. System rejects: "Order value below minimum required"
5. Order proceeds without discount

**Database Operations**:
- MongoDB: FIND promo code, check order_value < min_order_value
- SQL Server: INSERT Order with 0 discount

---

### **Scenario 6: First-Order-Only Promo Code**

**Existing Customer**:
1. Returning customer attempts to use "WELCOME10" (first-order-only)
2. System validates:
   - Code exists ✓
   - Code is active ✓
   - Usage limit OK ✓
   - Order value OK ✓
   - First-order-only check: Customer has 3 previous orders ✗
3. System rejects: "Only valid for first-time customers"
4. Order proceeds without discount

**Database Operations**:
- MongoDB: FIND promo code
- SQL Server: COUNT (SELECT COUNT(*) FROM Orders WHERE CustomerID = X) = 3
- SQL Server: INSERT Order with 0 discount

**New Customer**:
1. New customer attempts same "WELCOME10" code
2. All validations pass
3. Customer has 0 previous orders → First-order-only is valid ✓
4. Discount applied successfully
5. Order created with 10% discount

---

### **Scenario 7: Successful Order with Valid Discount**

**Flow**:
1. Customer selects product ($100)
2. Enters valid promo code "SUMMER20" (20% discount)
3. System validates all checks pass:
   - Code exists ✓
   - Code is active ✓
   - Usage limit OK ✓
   - Order value >= minimum ✓
   - First-order validation passes ✓
4. Discount calculation: $100 × 20% = $20 discount
5. Final amount: $80
6. Order inserted with:
   - ProductID, CustomerID, OrderDate
   - PromoCodeUsed: "SUMMER20"
   - TotalAmount: $80.00
7. MongoDB usage count incremented: usage_count += 1

**Database Operations**:
- MongoDB: FIND full promo code details
- SQL Server: INSERT Order with all details
- MongoDB: UPDATE usage_count (+1)

---

### **Scenario 8: SQL Server Unavailable (Graceful Degradation)**

**Flow**:
1. Application starts
2. tries to connect to SQL Server → Connection fails
3. Application warns: "SQL Server unavailable"
4. MongoDB connection succeeds
5. Sample products loaded (8 pre-defined items)
6. Application continues with MongoDB only
7. Customer registration/lookup skipped
8. Order creation fails (cannot save to SQL Server)
9. User can still browse and validate promotions

**Impact**:
- ✓ Product browsing works (sample data)
- ✓ Promo code validation works (MongoDB available)
- ✗ Customer creation skipped
- ✗ Order saving fails (no SQL Server)

---

### **Scenario 9: MongoDB Unavailable**

**Flow**:
1. Application starts
2. SQL Server connection succeeds
3. MongoDB connection fails → Error message
4. Application terminates (cannot proceed without MongoDB)

**Why Fail?**:
- Promo code validation requires MongoDB
- Cannot process orders without validation capability
- System is designed to fail-fast rather than operate incorrectly

---

### **Scenario 10: Multiple Consecutive Orders**

**Flow**:
1. Customer provides email (either new or existing)
2. **Order 1**: Selects product, applies promo, creates order
3. System asks: "Place another order?"
4. **Order 2**: User selects different product, no promo
5. Order created without discount
6. System asks again: "Place another order?"
7. User enters 'q' at product selection → Application exits
8. Database connections closed cleanly

**Database Operations**:
- Multiple INSERT operations to Orders table
- Multiple FIND/UPDATE operations to MongoDB
- All updates reflected in usage counts

---

## 🔗 DATABASE CONNECTIONS

### SQL Server Connection

**Configuration**:
```
Server: mcruebs04.isad.isadroot.ex.ac.uk
Database: BEMM459_2026_Group_Q
Username: Group_Q_2026
Encryption: YES (SSL/TLS)
Certificate Trust: YES
Timeout: 5 seconds
```

**Driver Fallback**:
1. Try ODBC Driver 18 for SQL Server (preferred)
2. If fails, try ODBC Driver 17 for SQL Server
3. If both fail, show troubleshooting tips

**Connection String**:
```
Driver={ODBC Driver 18 for SQL Server};
Server=mcruebs04.isad.isadroot.ex.ac.uk;
Database=BEMM459_2026_Group_Q;
UID=Group_Q_2026;
PWD=MrjV827*Wr;
Encrypt=yes;
TrustServerCertificate=yes;
Connection Timeout=5;
```

**Error Handling**:
- Attempts both ODBC driver versions
- Provides detailed troubleshooting if connection fails
- Application can continue with MongoDB-only if SQL fails

---

### MongoDB Connection

**Configuration**:
```
URI: mongodb://localhost:27017/
Database: promo_codes
Collection: promotions
Connection Timeout: 5000ms
```

**Connection String**:
```
mongodb://localhost:27017/
```

**Error Handling**:
- Tests connection with `ping` command
- Shows detailed error and troubleshooting tips if fails
- Application terminates if MongoDB unavailable (required)

---

## 👥 CUSTOMER MANAGEMENT

### Customer Lookup

**Process**:
1. User enters email address
2. Query SQL Server: `SELECT CustomerID FROM Customer WHERE Email = ?`
3. If found → Return existing CustomerID
4. If NOT found → Proceed with registration

**Validation**:
- Email cannot be empty
- Email must contain '@' symbol
- Minimum email format validation

---

### Customer Registration

**Process**:
1. Email not found in database
2. Prompt user for full name
3. Query SQL Server: `SELECT ISNULL(MAX(CustomerID), 0) + 1 FROM Customer`
4. Generate next available CustomerID
5. Insert new record:
   ```sql
   INSERT INTO Customer (CustomerID, Name, Email)
   VALUES (next_id, name, email)
   ```
6. Display confirmation with new CustomerID

**Validation**:
- Name cannot be empty
- Name must be at least 2 characters
- Email already validated in lookup step

**Error Handling**:
- If insert fails, show SQL error details
- Offer to continue without customer creation
- User can still browse and apply promos

---

### Customer Order History

**Purpose**: Check if customer is eligible for "first-order-only" promotions

**Process**:
1. Query SQL Server: `SELECT COUNT(*) FROM Orders WHERE CustomerID = ?`
2. Return order count (0 for new customers, >0 for returning)
3. Pass to promo validator for first-order-only check

**Used In**: PromoCodeValidator.validate_promo_code()

---

## 📦 PRODUCT MANAGEMENT

### Product Fetching

**Default Process**:
1. Query SQL Server: 
   ```sql
   SELECT ProductID, ProductName, Price FROM Products 
   ORDER BY ProductID
   ```
2. Store in memory as list of dictionaries:
   ```python
   {
     'id': ProductID,
     'name': ProductName,
     'price': Price (float)
   }
   ```

**Sample Data Fallback** (when SQL Server unavailable):
```
1. Wireless Mouse - $49.99
2. USB-C Cable - $15.99
3. Mechanical Keyboard - $99.99
4. Monitor Stand - $34.99
5. Desk Lamp - $29.99
6. Webcam HD - $79.99
7. External SSD 1TB - $129.99
8. USB Hub - $39.99
```

### Product Display

**Format**:
```
============================================================
AVAILABLE PRODUCTS
============================================================
1. Wireless Mouse                               $    49.99
2. USB-C Cable                                  $    15.99
3. Mechanical Keyboard                          $    99.99
4. Monitor Stand                                $    34.99
5. Desk Lamp                                    $    29.99
6. Webcam HD                                    $    79.99
7. External SSD 1TB                             $   129.99
8. USB Hub                                      $    39.99
============================================================
```

**Selection Validation**:
- User enters number (1-8)
- Invalid entries show error message
- User can enter 'q' to quit
- Valid selection returns product dictionary

---

## 🎫 PROMO CODE VALIDATION

### Four-Step Validation Process

The `PromoCodeValidator.validate_promo_code()` method performs comprehensive checks:

---

#### **Check 1: Code Existence**
```
MongoDB Query: db.promotions.findOne({"code": code})
Result: promo object found or None

If NOT found:
  ✗ Error: "Promo code '[code]' not found"
  → Validation fails, no discount applied
```

**Example**:
- User enters: "INVALID99"
- MongoDB search returns: NULL
- Result: Code rejected

---

#### **Check 2: Active Status**
```
MongoDB Field: active (boolean)
Value Required: true

If NOT active or missing:
  ✗ Error: "Promo code '[code]' is no longer active"
  → Validation fails, no discount applied
```

**Example**:
- User enters: "OLDPROMO"
- Code found BUT active = FALSE
- Result: Code rejected (expired)

---

#### **Check 3: Usage Limit**
```
MongoDB Fields: 
  - usage_count (current uses)
  - max_uses (maximum allowed uses)

Validation: usage_count < max_uses

If limit reached:
  ✗ Error: "Promo code '[code]' has reached maximum uses"
  → Validation fails, no discount applied
```

**Example**:
- Promo "SUMMER20" has max_uses = 100
- Current usage_count = 100
- Result: Code rejected (exhausted)

---

#### **Check 4: Minimum Order Value**
```
MongoDB Field: min_order_value (decimal)
Validation: order_value >= min_order_value

If order too small:
  ✗ Error: "Order value $[amount] below minimum required $[min]"
  → Validation fails, no discount applied
```

**Example**:
- Promo requires minimum $50 order
- User's order is $35
- Result: Code rejected (order too small)

---

#### **Check 5: First-Order-Only Rule**
```
MongoDB Field: rules.first_order_only (boolean)
SQL Server Query: SELECT COUNT(*) FROM Orders WHERE CustomerID = ?

Validation: 
  IF first_order_only = true:
    MUST have order_count = 0

If customer is not first-time:
  ✗ Error: "Promo '[code]' only valid for first-time customers"
  → Validation fails, no discount applied
```

**Example - New Customer**:
- "WELCOME10" has first_order_only = true
- Customer order count = 0
- Result: Code ACCEPTED ✓

**Example - Returning Customer**:
- Same "WELCOME10" code
- Customer order count = 3
- Result: Code REJECTED ✗

---

### Successful Validation Response

When all 5 checks pass:
```python
{
  'code': 'SUMMER20',
  'active': True,
  'discount_percent': 20,
  'usage_count': 50,
  'max_uses': 100,
  'min_order_value': 0,
  'rules': {'first_order_only': False},
  ...additional fields...
}
```

**Console Output**:
```
[OK] Valid promo code! Discount: 20%
```

---

### Usage Count Update

When promo code is validated successfully:
```
MongoDB Update: 
  db.promotions.updateOne(
    {"code": promo_code},
    {"$inc": {"usage_count": 1}}
  )
```

**Purpose**: Track how many times the code has been used
**Timing**: After validation, before order creation
**Atomic Operation**: $inc operator ensures thread-safe increment

---

## 🛒 ORDER PROCESSING

### Order Creation Workflow

**Step 1: Generate Unique OrderID**
```sql
SELECT ISNULL(MAX(OrderID), 0) + 1 FROM Orders
```
- Gets next available ID
- Ensures no duplicate orders

---

**Step 2: Calculate Discount**
```python
IF promo_code:
  discount_amount = product_price × (discount_percent / 100)
  total_amount = product_price - discount_amount
ELSE:
  total_amount = product_price
```

**Example**:
- Product: $100, Discount: 20%
- Calculation: $100 - ($100 × 20%) = $100 - $20 = $80

---

**Step 3: Validate CustomerID**
```python
IF customer_id is None OR customer_id == 0:
  ✗ Error: "Cannot create order - Customer ID invalid"
  → Order creation fails
```

---

**Step 4: Database Insertion**
```sql
INSERT INTO Orders 
  (OrderID, CustomerID, OrderDate, PromoCodeUsed, TotalAmount)
VALUES 
  (next_order_id, customer_id, today_date, promo_code or NULL, total_amount)
```

**Success Response**:
```
[OK] Order created successfully in SQL Server!
  - OrderID: 1001
  - Order Amount: $100.00
  - Discount (20%): -$20.00
  - Total Amount: $80.00
```

---

**Step 5: Commit Transaction**
```python
self.sql_connection.commit()
```

- Ensures order is permanently saved
- Makes changes visible to other queries

---

### Order Details Stored

| Field | Value | Source |
|-------|-------|--------|
| OrderID | Auto-generated | SQL Server query |
| CustomerID | From lookup/registration | Customer management |
| OrderDate | Today's date | datetime.now().date() |
| PromoCodeUsed | User input (uppercase) | Promo validator |
| TotalAmount | Calculated with discount | Discount calculation |

---

### Error Handling in Order Creation

**Scenario 1: SQL Server Not Connected**
```
[ERROR] SQL Server not connected. Order simulated (not saved).
```
- Order not persisted
- Application continues
- Allows MongoDB-only operation

---

**Scenario 2: Invalid CustomerID**
```
[ERROR] Cannot create order - Customer ID is invalid
Debug: customer_id = None
```
- Customer creation failed earlier
- Need to register customer successfully first

---

**Scenario 3: SQL Insert Fails**
```
[ERROR] Failed to save order to SQL Server
Details: [SQL Server error message]

Troubleshooting:
1. Verify CustomerID X exists in the Customers table
2. Check for foreign key constraints on Orders table
3. Ensure all required fields are valid

Order details that failed to save:
  - OrderID: 1001
  - CustomerID: 100
  - OrderDate: 2026-03-27
  - PromoCodeUsed: SUMMER20
  - TotalAmount: $80.00
```

**Common Causes**:
- Foreign key constraint (CustomerID doesn't exist)
- Table name or column name mismatch
- Data type mismatch (decimal vs float)
- Permission issues

---

## ⚠️ ERROR HANDLING

### Connection Errors

**SQL Server Connection Fails**:
```
[ERROR] Error connecting to SQL Server

Troubleshooting tips:
1. Ensure you have ODBC Driver 18 or 17 for SQL Server installed
2. Server requires Encrypt=yes and TrustServerCertificate=yes
3. Check your server name, username, and password
4. Verify your database exists on the server
```

**Application Response**: Warns user, continues with MongoDB only

---

**MongoDB Connection Fails**:
```
[ERROR] Error connecting to MongoDB: [error details]

Troubleshooting tips:
1. Ensure MongoDB is running locally on port 27017
2. Check if MongoDB service is installed and started
3. On Windows, start MongoDB with: mongod
```

**Application Response**: Terminates (required service)

---

### Validation Errors

**All validation errors during promo check**:
```
[ERROR] Promo code '[code]' [reason]
[ERROR] Order value $X below minimum required $Y
[ERROR] Promo code '[code]' not found
[ERROR] Promo code '[code]' is no longer active
[ERROR] Promo code '[code]' has reached maximum uses
[ERROR] Promo code '[code]' only valid for first-time customers
```

**Application Response**: Continue without discount

---

### Customer Management Errors

**Email Validation**:
```
[ERROR] Email cannot be empty
[ERROR] Invalid email format
```

**Name Validation**:
```
[ERROR] Name cannot be empty
[ERROR] Name must be at least 2 characters
```

**Customer Creation Fails**:
```
[ERROR] Failed to create customer: [SQL error details]
[!] Account creation failed. You can still browse, but orders may not save.
    Proceeding without SQL Server customer creation...
```

---

### Order Creation Errors

**Missing Customer**:
```
[ERROR] Cannot create order - Customer ID is invalid
```

**SQL Insert Fails**:
```
[ERROR] Failed to save order to SQL Server
Details: [SQL error with line numbers]
```

---

### Exception Handling Strategies

1. **Try-Except Blocks**: Wrap all database operations
2. **Specific Error Messages**: Show what went wrong
3. **Graceful Degradation**: Continue with available services
4. **User Guidance**: Provide troubleshooting tips
5. **Fail-Fast**: Terminate if critical service unavailable
6. **Logging**: Print detailed error information

---

## ⚙️ CONFIGURATION

### Database Credentials

**SQL Server** (in `DatabaseConnection.__init__`):
```python
self.sql_server = "mcruebs04.isad.isadroot.ex.ac.uk"
self.sql_database = "BEMM459_2026_Group_Q"
self.sql_username = "Group_Q_2026"
self.sql_password = "MrjV827*Wr"
```

**MongoDB** (in `DatabaseConnection.__init__`):
```python
self.mongo_uri = "mongodb://localhost:27017/"
self.mongo_db = "promo_codes"
self.mongo_collection = "promotions"
```

---

### Connection String Parameters

**SQL Server SSL Settings**:
- `Encrypt=yes` → Enable SSL/TLS encryption
- `TrustServerCertificate=yes` → Trust the server's certificate
- `Connection Timeout=5` → 5-second timeout for SSL handshake

**MongoDB Timeout**:
- `serverSelectionTimeoutMS=5000` → 5-second server selection timeout

---

### Sample Product Data

Used when SQL Server is unavailable:
```python
self.product_manager.products = [
    {'id': 1, 'name': 'Wireless Mouse', 'price': 49.99},
    {'id': 2, 'name': 'USB-C Cable', 'price': 15.99},
    {'id': 3, 'name': 'Mechanical Keyboard', 'price': 99.99},
    {'id': 4, 'name': 'Monitor Stand', 'price': 34.99},
    {'id': 5, 'name': 'Desk Lamp', 'price': 29.99},
    {'id': 6, 'name': 'Webcam HD', 'price': 79.99},
    {'id': 7, 'name': 'External SSD 1TB', 'price': 129.99},
    {'id': 8, 'name': 'USB Hub', 'price': 39.99}
]
```

---

## 🚀 RUNNING THE APPLICATION

### Prerequisites

1. **Python 3.7+** installed
2. **ODBC Driver 18 or 17** for SQL Server (optional)
3. **MongoDB** running locally on port 27017
4. **Python packages** installed:
   ```bash
   pip install pyodbc pymongo
   ```

---

### Starting the Application

```bash
python order_management_system.py
```

---

### Application Flow

```
1. Initialize connections to SQL Server and MongoDB
2. Display welcome message
3. Prompt user for email address:
   - Enter existing customer email → Login
   - Enter new email → Register with name
4. Display available products (8 items)
5. Prompt to select product
6. Offer optional promo code
7. Process and create order
8. Ask: "Place another order?"
   - Yes → Go to step 4
   - No → Proceed to cleanup
9. Close all database connections
10. Display "Application closed successfully"
```

---

### User Controls

| Command | Action |
|---------|--------|
| Enter email | Authenticate or register |
| Enter name | Complete new customer registration |
| Enter product number (1-8) | Select product for order |
| Enter promo code | Apply discount code (optional) |
| Press Enter (promo) | Skip promo code (no discount) |
| Enter 'yes' or 'y' | Place another order |
| Enter anything else | Exit application |
| Press Ctrl+C | Force exit (safe shutdown) |

---

### Expected Console Output

**Successful Run**:
```
============================================================
ORDER MANAGEMENT SYSTEM - Polyglot Persistence Demo
============================================================

Initializing connections...
[OK] Successfully connected to SQL Server (using ODBC Driver 18 for SQL Server)
[OK] Successfully connected to MongoDB

[OK] Fetched 8 products from database

============================================================
WELCOME TO ORDER MANAGEMENT SYSTEM
============================================================

Enter your email address: john@example.com
[OK] Customer found! Welcome back

============================================================
AVAILABLE PRODUCTS
============================================================
1. Wireless Mouse                               $    49.99
...
============================================================

Select a product (enter number): 1

============================================================
Product Selected: Wireless Mouse
Price: $49.99
============================================================

Enter promo code (or press Enter to skip): SUMMER20
[OK] Valid promo code! Discount: 20%

[OK] Order created successfully in SQL Server!
  - OrderID: 1
  - Order Amount: $49.99
  - Discount (20%): -$9.99
  - Total Amount: $40.00

Place another order? (yes/no): no

Closing database connections...
[OK] Application closed successfully
```

---

### Troubleshooting

**MongoDB Not Running**:
```
[ERROR] Error connecting to MongoDB: ...
Troubleshooting tips:
1. Ensure MongoDB is running locally on port 27017
```
→ Start MongoDB: `mongod` in PowerShell

---

**ODBC Driver Missing**:
```
[ERROR] Error connecting to SQL Server
Troubleshooting tips:
1. Ensure you have ODBC Driver 18 or 17 for SQL Server installed
```
→ Install from Microsoft: ODBC Driver 18 for SQL Server

---

**SQL Server Timeout**:
```
[!] SQL Server unavailable. Running with MongoDB only.
```
→ Check server connection: `ping mcruebs04.isad.isadroot.ex.ac.uk`

---

## 📊 DATABASE TABLES REQUIRED

### SQL Server - Customer Table
```sql
CREATE TABLE Customer (
    CustomerID INT PRIMARY KEY,
    Name NVARCHAR(255),
    Email NVARCHAR(255) UNIQUE
)
```

---

### SQL Server - Products Table
```sql
CREATE TABLE Products (
    ProductID INT PRIMARY KEY,
    ProductName NVARCHAR(255),
    Price DECIMAL(10, 2)
)
```

---

### SQL Server - Orders Table
```sql
CREATE TABLE Orders (
    OrderID INT PRIMARY KEY,
    CustomerID INT FOREIGN KEY REFERENCES Customer(CustomerID),
    OrderDate DATE,
    PromoCodeUsed NVARCHAR(50) NULL,
    TotalAmount DECIMAL(10, 2)
)
```

---

### MongoDB - Promotions Collection

**Sample Document**:
```json
{
  "_id": ObjectId("..."),
  "code": "SUMMER20",
  "active": true,
  "discount_percent": 20,
  "usage_count": 45,
  "max_uses": 100,
  "min_order_value": 0,
  "rules": {
    "first_order_only": false
  }
}
```

**Sample Document (First-Order Only)**:
```json
{
  "_id": ObjectId("..."),
  "code": "WELCOME10",
  "active": true,
  "discount_percent": 10,
  "usage_count": 12,
  "max_uses": 50,
  "min_order_value": 25,
  "rules": {
    "first_order_only": true
  }
}
```

---

## 📈 POLYGLOT PERSISTENCE BENEFITS DEMONSTRATED

| Aspect | SQL Server (Relational) | MongoDB (Document) | Benefit |
|--------|------------------------|-------------------|---------|
| **Data Structure** | Fixed schema | Flexible schema | Different data types |
| **Transactions** | ACID compliant | Single document atomic | Different guarantee needs |
| **Update Speed** | TableLocks | Atomic operators | Different performance needs |
| **Scale Type** | Vertical | Horizontal | Different scalability |
| **Use Case** | Structured orders | Dynamic promotions | Polyglot approach |

---

## 🎓 LEARNING OUTCOMES

This application demonstrates:

1. **Multiple database integration** - SQL Server + MongoDB together
2. **Error handling** - Graceful degradation and fallbacks
3. **Object-oriented design** - Separated concerns across classes
4. **Data validation** - Multiple-step validation logic
5. **User interaction** - Interactive CLI application
6. **Transaction management** - Order atomicity
7. **Connection pooling** - Proper resource management

---

## 📝 NOTES

- No changes are made to Python code when using this README
- All scenarios describe existing functionality
- Error messages are copied directly from code
- Database queries are exact SQL used in application
- Configuration values match actual implementation

