# MongoDB Setup Guide - Promo Code Database

## 📋 Overview

This MongoDB instance stores promotional code data for a polyglot persistence e-commerce application. The database uses document-based storage to maintain flexible promo code schemas with nested promotional rules and conditions.

**Database Name:** `promo_codes`  
**Collection Name:** `promotions`  
**Connection String:** `mongodb://localhost:27017/`

---

## 🚀 Quick Start

### ⭐ Primary Tool: Admin Promo Manager

The easiest way to manage your promo codes is using **admin_promo_manager.py**:

```bash
python admin_promo_manager.py
```

This interactive tool allows you to:
- ✅ View all promo codes
- ✅ View detailed code information
- ✅ Add new promo codes
- ✅ Update existing codes
- ✅ Deactivate codes
- ✅ Check usage statistics

**No MongoDB shell knowledge required!**

---

### 1. Prerequisites
- MongoDB Server (local or remote)
- Python 3.7+ (for Python setup scripts)
- MongoDB Compass (optional, for GUI management)

### 2. Connection Details

**MongoDB Compass Connection:**
```json
{
  "connectionString": "mongodb://localhost:27017/",
  "type": "Compass Connections",
  "database": "promo_codes",
  "collection": "promotions"
}
```

**Import Compass Connections:**
1. Use the provided `compass-connections (1).json` file
2. Open MongoDB Compass → Import connections
3. Select the JSON file to import

### 3. Initialize Database

#### Option A: Using Python Setup Script (Recommended)

```bash
cd NoSQL
python ../setup_mongodb_data.py
```

This will:
- Connect to the local MongoDB instance
- Create the `promo_codes` database
- Insert sample promo code documents
- Create an index on the `code` field for optimized searches

#### Option B: Using MongoDB Shell Script (Alternative)

```bash
mongosh
use promo_codes
# Copy and paste the contents of mongodb_setup.js
```

---

## 📊 Database Schema

### Collection: `promotions`

Each promotional code document follows this structure:

```json
{
  "_id": "promo_SUMMER20",
  "code": "SUMMER20",
  "discount_percent": 20,
  "brand_id": 1,
  "brand_name": "TechZone",
  "expiry_date": "2025-08-31",
  "channel": "email",
  "campaign": "Summer Sale",
  "min_order_value": 30,
  "applicable_product_ids": [1, 2, 3, 4],
  "customer_types": ["new", "existing"],
  "active": true,
  "usage_count": 0,
  "max_uses": 500,
  "created_at": "2025-01-01",
  "rules": {
    "min_purchase": 30,
    "max_discount": 500,
    "stackable": false
  }
}
```

### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `_id` | String | Unique identifier (format: `promo_[CODE]`) |
| `code` | String | Promotional code to be used by customers |
| `discount_percent` | Number | Discount percentage (0-100) |
| `brand_id` | Number | Associated brand identifier |
| `brand_name` | String | Brand name |
| `expiry_date` | String | Expiration date (YYYY-MM-DD format) |
| `channel` | String | Distribution channel (email, website, promotional) |
| `campaign` | String | Campaign name/description |
| `min_order_value` | Number | Minimum order value to apply promo |
| `applicable_product_ids` | Array | List of product IDs eligible for this promo |
| `customer_types` | Array | Customer types eligible (new, existing) |
| `active` | Boolean | Whether the promo code is currently active |
| `usage_count` | Number | Current usage count |
| `max_uses` | Number | Maximum allowed uses |
| `created_at` | String | Creation date (YYYY-MM-DD format) |
| `rules` | Object | Additional business rules (min_purchase, max_discount, stackable) |

---

## 📝 Sample Data

The database includes 4 sample promo codes:

### 1. SUMMER20 (TechZone)
- **Discount:** 20%
- **Expiry:** 2025-08-31
- **Min Order:** $30
- **Max Uses:** 500
- **Eligible:** New & Existing customers

### 2. WELCOME10 (TechZone)
- **Discount:** 10%
- **Expiry:** 2025-12-31
- **Min Order:** $20
- **Max Uses:** 1,000
- **Eligible:** New customers only

### 3. TECH25 (ElectroHub)
- **Discount:** 25%
- **Expiry:** 2025-04-30
- **Min Order:** $50
- **Max Uses:** 300
- **Eligible:** Existing customers only

### 4. FLASH15 (GadgetWorld)
- **Discount:** 15%
- **Expiry:** 2025-03-31
- **Min Order:** $25
- **Max Uses:** 100
- **Eligible:** New & Existing customers

---

## 💻 Common Operations

### Using Admin Promo Manager (Python) - Primary Tool

The **admin_promo_manager.py** is your main tool for managing promo codes:

```bash
python admin_promo_manager.py
```

**Available Functions:**
- **View All Promo Codes** - Display all active and inactive promos
- **View Promo Details** - Get detailed information about a specific code
- **Add New Promo Code** - Create a new promotional code interactively
- **Update Promo Code** - Modify existing code details
- **Deactivate Promo Code** - Disable a promo without deleting it
- **View Usage Statistics** - Check how many times each code was used

### Python Code Examples

**View All Promo Codes:**
```python
from admin_promo_manager import PromoCodeManager

manager = PromoCodeManager()
manager.connect()
promos = manager.view_all_promos()
manager.disconnect()
```

**View Specific Promo Details:**
```python
manager.connect()
promo = manager.view_promo_details("SUMMER20")
manager.disconnect()
```

**Add New Promo Code:**
```python
manager.connect()
manager.add_promo_code()
manager.disconnect()
```

**Update Usage Count:**
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['promo_codes']
collection = db['promotions']

collection.update_one(
    {"code": "SUMMER20"},
    {"$inc": {"usage_count": 1}}
)
```

**Query Promo Codes by Status:**
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client['promo_codes']
collection = db['promotions']

# Get only active promos
active_promos = list(collection.find({"active": True}))

# Get promos with usage < max uses
available = list(collection.find({
    "$expr": {"$lt": ["$usage_count", "$max_uses"]}
}))
```

### Display Data (Python Script)

```bash
python show_mongodb_data.py
```



---

## 📑 Files Structure

```
NoSQL/
├── mongodb_setup.js              # MongoDB shell script to initialize database
├── README_MONGODB.md             # This file
```

### Supporting Python Files (Parent Directory)
```
├── admin_promo_manager.py*      # PRIMARY: Interactive promo code management tool
├── setup_mongodb_data.py        # Initialize database with sample data
├── show_mongodb_data.py         # Display all promo codes
└── order_management_system.py   # Main application using MongoDB
```
*Main tool for managing promo codes

---

## 🔍 Indexes

An index is automatically created on the `code` field for optimized lookups:

```javascript
db.promotions.createIndex({ "code": 1 }, { unique: true })
```

**Benefits:**
- Fast queries by promo code
- Ensures code uniqueness
- Improved application performance

### View Existing Indexes

```javascript
db.promotions.getIndexes()
```

---

## 🛠️ Maintenance Tasks

### Using Admin Promo Manager (Recommended)

```bash
# Interactive interface for all management tasks
python admin_promo_manager.py
```

### Python Script Commands

**Count Documents:**
```python
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
collection = client['promo_codes']['promotions']
count = collection.count_documents({})
print(f"Total promo codes: {count}")
```

**Clear All Data:**
```python
collection.delete_many({})
```

**Reset Usage Counts:**
```python
collection.update_many({}, {"$set": {"usage_count": 0}})
```

### MongoDB Shell Commands

**Count Documents:**
```javascript
db.promotions.countDocuments({})
```

**Clear All Data:**
```javascript
db.promotions.deleteMany({})
```

**Reset Usage Counts:**
```javascript
db.promotions.updateMany({}, {"$set": {"usage_count": 0}})
```

**Export Data (JSON):**
```bash
mongoexport --db promo_codes --collection promotions --out promotions_backup.json
```

**Import Data From Backup:**
```bash
mongoimport --db promo_codes --collection promotions --file promotions_backup.json
```

---

## 📦 Integration with Application

### Main Integration: Admin Promo Manager

The **admin_promo_manager.py** is your primary tool for all promo code operations:

```bash
# Run the admin interface
python admin_promo_manager.py
```

**Key Features:**
- Interactive menu-driven interface
- Add, view, update, and manage promo codes
- Track usage statistics
- Validate promo code rules

### Direct Python Integration

For programmatic access, use PyMongo directly:

```python
from pymongo import MongoClient

# Connect to database
client = MongoClient('mongodb://localhost:27017/')
db = client['promo_codes']
collection = db['promotions']

# Validate promo code
promo = collection.find_one({"code": "SUMMER20"})
if promo and promo['active']:
    discount = promo['discount_percent']
    # Apply discount to order
    
# Update usage
collection.update_one(
    {"code": "SUMMER20"},
    {"$inc": {"usage_count": 1}}
)
```

### Integration in Order Management System

The `order_management_system.py` uses MongoDB to validate and apply promo codes:

---

## ⚠️ Troubleshooting

### Connection Issues

**Problem:** Cannot connect to MongoDB

**Solutions:**
1. Verify MongoDB is running: `mongosh`
2. Check connection string: `mongodb://localhost:27017/`
3. Ensure port 27017 is not blocked

### No Data Found

**Problem:** Database is empty

**Solutions:**
1. Run setup script: `python setup_mongodb_data.py`
2. Check if MongoDB is running

### Index Already Exists

**Problem:** Error when creating index again

**Solution:**
Drop the old index before creating a new one, or use MongoDB Compass to manage indexes.

### Duplicate Key Error

**Problem:** Cannot insert promo code with existing code value

**Solution:**
```javascript
db.promotions.deleteOne({ code: "DUPLICATE_CODE" })
// Then insert the new document
```

---

## 🔐 Best Practices

1. **Always use indexes** on frequently queried fields
2. **Validate data** before insertion (code format, discount range)
3. **Regular backups** of promo code data
4. **Use unique constraints** on code field to prevent duplicates
5. **Monitor usage counts** to track promotions effectiveness
6. **Archive expired codes** instead of permanent deletion
7. **Use transactions** for complex multi-document updates
8. **Document schema changes** when modifying structure

---

## 📊 Performance Tips

- Use `.explain()` to analyze query performance
- Create indexes before running heavy queries
- Use projection to retrieve only needed fields
- Batch operations when possible
- Monitor database size with `db.hostInfo()`

---

## 🔗 Related Files

For complete project structure and SQL integration, see:
- `README.md` - Main project documentation
- `SQL/` - Relational database setup scripts
- `order_management_system.py` - Main application
- `SETUP_GUIDE.md` - Complete system setup guide

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section above
2. Review MongoDB official documentation: https://docs.mongodb.com/
3. Consult the main project README for system-wide issues

---

**Last Updated:** March 2026  
**Database Version:** MongoDB 5.0+  
**Python Driver:** pymongo 4.0+
