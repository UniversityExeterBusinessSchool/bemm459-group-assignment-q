# Admin Promo Code Management System - README

## 📋 Overview

The **Admin Promo Code Management System** (`admin_promo_manager.py`) is an interactive command-line tool for managing promotional codes in MongoDB. It provides a user-friendly interface for administrators to add, view, edit, and manage promo codes without requiring database knowledge.

**Type:** Interactive CLI Application  
**Language:** Python 3.7+  
**Database:** MongoDB (promo_codes database)  
**Default Connection:** `mongodb://localhost:27017/`

---

## 🚀 Quick Start

### 1. Prerequisites

Before running the admin manager, ensure you have:

- ✅ Python 3.7 or higher installed
- ✅ MongoDB running locally (or accessible at connection string)
- ✅ PyMongo library installed
- ✅ Sample data loaded in MongoDB (optional, but recommended)

### 2. Install Dependencies

```bash
pip install pymongo
```

### 3. Launch the Application

```bash
python admin_promo_manager.py
```

You'll see the welcome screen:

```
================================================================================
ADMIN PROMO CODE MANAGEMENT SYSTEM
================================================================================

--------------------------------------------------------------------------------
MAIN MENU
--------------------------------------------------------------------------------
1. View all promo codes
2. View promo code details
3. Add new promo code
4. Edit promo code
5. Delete promo code
6. Reset usage count
0. Exit

Select option (0-6):
```

---

## 📱 Features & Usage

### Option 1: View All Promo Codes

Displays a list of all promotional codes in the database with key information.

**How to use:**
```
Select option (0-6): 1
```

**Output Example:**
```
================================================================================
ALL PROMO CODES
================================================================================

1. Code: SUMMER20
   Discount: 20%
   Campaign: Summer Sale
   Active: True
   First Order Only: False
   Type: percentage_discount
   Min Order Value: $30.00
   Max Uses: 500
   Usage Count: 125

2. Code: WELCOME10
   Discount: 10%
   Campaign: Welcome New Customers
   Active: True
   First Order Only: True
   Type: percentage_discount
   Min Order Value: $20.00
   Max Uses: 1000
   Usage Count: 342
```

**Information Displayed:**
- `Code` - The promotional code
- `Discount` - Discount percentage
- `Campaign` - Campaign name
- `Active` - Whether the code is currently active
- `First Order Only` - If restricted to new customers only
- `Type` - Type of discount (e.g., percentage_discount)
- `Min Order Value` - Minimum purchase required
- `Max Uses` - Maximum number of times the code can be used
- `Usage Count` - How many times the code has been used

---

### Option 2: View Promo Code Details

Shows comprehensive information about a specific promo code.

**How to use:**
```
Select option (0-6): 2
Enter promo code: SUMMER20
```

**Output Example:**
```
================================================================================
PROMO CODE DETAILS: SUMMER20
================================================================================

Code: SUMMER20
Discount: 20%
Campaign: Summer Sale
Description: Limited time summer promotion
Active: True
Min Order Value: $30.00
Max Uses: 500
Current Usage: 125

Rules:
  Type: percentage_discount
  First Order Only: False
  Exclude Categories: []
```

**Information Displayed:**
- Full promo code details
- Campaign name and description
- Active status
- Order requirements
- Usage limits and current usage
- Detailed business rules

---

### Option 3: Add New Promo Code

Creates a new promotional code with custom settings.

**How to use:**
```
Select option (0-6): 3
```

**Interactive Input:**
```
================================================================================
ADD NEW PROMO CODE
================================================================================

Enter promo code (e.g., SUMMER20): FLASH30
Enter discount percentage (e.g., 20): 30
Enter campaign name (e.g., Summer Sale): Flash Sale 2026
Enter description (optional): 30% off all electronics
Enter minimum order value (default 0): 50
Enter maximum uses (leave blank for unlimited): 200
Is this promo code active? (yes/no, default yes): yes
First order only? (yes/no, default no): no
```

**Confirmation:**
```
[OK] Promo code 'FLASH30' added successfully!
    Discount: 30%
    Campaign: Flash Sale 2026
    First Order Only: False
```

**Input Guide:**
| Field | Type | Example | Notes |
|-------|------|---------|-------|
| Promo Code | String | `FLASH30` | Must be unique, converted to uppercase |
| Discount % | Number | `30` | 0-100 percentage |
| Campaign Name | String | `Flash Sale 2026` | Descriptive name |
| Description | String | `30% off electronics` | Optional field |
| Min Order Value | Number | `50` | Minimum purchase to apply code |
| Max Uses | Number | `200` | Leave blank for unlimited |
| Active | Yes/No | `yes` | Activate immediately or wait |
| First Order Only | Yes/No | `no` | Restrict to new customers |

---

### Option 4: Edit Promo Code

Modify an existing promo code with selective field updates.

**How to use:**
```
Select option (0-6): 4
Enter promo code to edit (e.g., SUMMER20): SUMMER20
```

**Current Details Display:**
```
Current details for SUMMER20:
  Discount: 20%
  Campaign: Summer Sale
  Active: True
  Min Order Value: $30.00
  First Order Only: False
```

**Edit Menu:**
```
--------------------------------------------------------------------------------
What would you like to edit?
1. Discount percentage
2. Campaign name
3. Description
4. Active status
5. Minimum order value
6. First order only status
7. Maximum uses
0. Cancel

Select (0-7): 1
Enter new discount percentage: 25
```

**Confirmation:**
```
[OK] Promo code 'SUMMER20' updated successfully!
```

**Editable Fields:**
1. **Discount percentage** - Change discount amount
2. **Campaign name** - Update campaign title
3. **Description** - Add or modify promo description
4. **Active status** - Enable/disable the code
5. **Minimum order value** - Change purchase requirement
6. **First order only** - Toggle new customer restriction
7. **Maximum uses** - Adjust usage limit

---

### Option 5: Delete Promo Code

Permanently remove a promo code from the database.

**How to use:**
```
Select option (0-6): 5
Enter promo code to delete: OLDPROMO
```

**Confirmation Required:**
```
Are you sure you want to delete 'OLDPROMO'? (yes/no): yes

[OK] Promo code 'OLDPROMO' deleted successfully!
```

⚠️ **Warning:** This action is permanent and cannot be undone. Use with caution!

---

### Option 6: Reset Usage Count

Reset the usage counter for a promo code back to zero.

**How to use:**
```
Select option (0-6): 6
Enter promo code to reset usage: SUMMER20

[OK] Usage count reset for 'SUMMER20'
```

**Use Cases:**
- Start a new campaign cycle
- Clear usage for seasonal promotions
- Audit tracking

---

### Option 0: Exit

Closes the admin panel and disconnects from MongoDB.

```
Select option (0-6): 0

[OK] Exiting admin panel...
[OK] Disconnected from MongoDB
[OK] Admin panel closed
```

---

## 🗄️ Data Structure

### Promo Code Document Format

When you add or edit a promo code, it's stored in MongoDB with this structure:

```json
{
  "_id": "ObjectId",
  "code": "SUMMER20",
  "discount_percent": 20,
  "campaign": "Summer Sale",
  "description": "Limited time summer promotion",
  "active": true,
  "min_order_value": 30,
  "max_uses": 500,
  "usage_count": 125,
  "rules": {
    "type": "percentage_discount",
    "first_order_only": false,
    "exclude_categories": []
  },
  "created_at": "2026-03-27T10:30:00.000Z",
  "updated_at": "2026-03-27T14:45:00.000Z"
}
```

### Field Reference

| Field | Type | Description |
|-------|------|-------------|
| `code` | String | Unique promotional code (uppercase) |
| `discount_percent` | Number | Discount value (0-100) |
| `campaign` | String | Campaign name/identifier |
| `description` | String | Detailed campaign description |
| `active` | Boolean | Whether code is currently usable |
| `min_order_value` | Number | Minimum order amount to use code |
| `max_uses` | Number | Maximum redemptions allowed |
| `usage_count` | Number | Current number of uses |
| `rules` | Object | Additional promotion rules |
| `rules.type` | String | Type of discount (e.g., percentage_discount) |
| `rules.first_order_only` | Boolean | Restrict to new customers only |
| `rules.exclude_categories` | Array | Product categories excluded from discount |
| `created_at` | DateTime | When code was created |
| `updated_at` | DateTime | Last modification time |

---

## ⚙️ Configuration

### Modify Database Connection

To connect to a different MongoDB instance, edit the connection parameters in the code:

```python
def __init__(self):
    """Initialize MongoDB connection"""
    self.mongo_uri = "mongodb://localhost:27017/"  # Change this
    self.mongo_db_name = "promo_codes"             # Or this
    self.mongo_collection_name = "promotions"      # Or this
```

**Examples:**
```python
# Remote MongoDB
self.mongo_uri = "mongodb://user:password@remote-host:27017/"

# MongoDB Atlas
self.mongo_uri = "mongodb+srv://user:password@cluster.mongodb.net/database?retryWrites=true&w=majority"

# Different database
self.mongo_db_name = "my_promotions"
```

---

## 🔍 Workflow Examples

### Example 1: Create a New Flash Sale Promotion

```
1. Launch the manager:
   python admin_promo_manager.py

2. Select option 3 (Add new promo code)

3. Enter details:
   - Code: FLASH50
   - Discount: 50
   - Campaign: Flash Sale Week 1
   - Description: 50% off selected items
   - Min Order: 25
   - Max Uses: 150
   - Active: yes
   - First Order Only: no

4. Promo created and ready to use!
```

### Example 2: Update Discount During Campaign

```
1. Select option 4 (Edit promo code)

2. Enter code: SUMMER20

3. Select option 1 (Edit discount)

4. Update from 20% to 25%

5. Changes saved to database
```

### Example 3: Deactivate Expired Promotion

```
1. Select option 4 (Edit promo code)

2. Enter code: OLDPROMO

3. Select option 4 (Edit active status)

4. Change to 'no'

5. Code is now inactive (not usable by customers)
```

### Example 4: Check Campaign Performance

```
1. Select option 2 (View details)

2. Enter code: SUMMER20

3. View usage count vs max uses

4. Example output:
   Max Uses: 500
   Current Usage: 425
   (Code has been used 425 times out of 500 allowed)
```

---

## ⚠️ Common Issues & Solutions

### Connection Errors

**Problem:** `[ERROR] Failed to connect to MongoDB: ...`

**Solutions:**
1. Verify MongoDB is running:
   ```bash
   mongosh  # or: mongo (older versions)
   ```
2. Check connection string is correct
3. Ensure port 27017 is not blocked
4. Verify MongoDB credentials if using authentication

### Promo Code Not Found

**Problem:** `[ERROR] Promo code 'XXX' not found!`

**Solutions:**
1. Check the exact spelling (case-sensitive on display, but codes are uppercase)
2. Verify code exists: Select option 1 to view all codes
3. Code may have been deleted previously

### Duplicate Code Error

**Problem:** `[ERROR] Promo code 'SUMMER20' already exists!`

**Solutions:**
1. Use a different code name
2. Edit the existing code instead of creating a new one (Option 4)
3. Delete the old code if it's no longer needed (Option 5)

### Invalid Input

**Problem:** `[ERROR] Invalid input: ...`

**Solutions:**
1. Enter numeric values for percentage/price fields
2. Don't use special characters in promo codes (use alphanumeric only)
3. Dates should be in YYYY-MM-DD format if required
4. Yes/No prompts: type 'yes' or 'no' (case-insensitive)

### Database Connection Timeout

**Problem:** Long delay or timeout when connecting

**Solutions:**
1. Check network connection
2. MongoDB server may be busy - wait and retry
3. Increase timeout in configuration (default 5000ms)
4. Check MongoDB server logs for errors

---

## 🎯 Best Practices

### 1. Code Naming Convention

Use descriptive, uppercase codes with the discount or period:
```
✅ GOOD:  SUMMER20, FLASH50, WELCOME10, NEWYEAR30
❌ BAD:   s20, f, promo1, xyz
```

### 2. Campaign Naming

Include relevant details in campaign name:
```
✅ GOOD:  "Summer Sale 2026", "New Customer Welcome", "Holiday Special Week 1"
❌ BAD:   "Promo", "Sale", "Campaign"
```

### 3. Usage Limits

Set realistic max uses based on campaign scope:
```
- Targeted campaigns: 50-200 uses
- Broad promotions: 500-1000 uses
- Limited time: 100-300 uses
```

### 4. Minimum Order Values

Ensure they're profitable but attractive:
```
- Most products: $20-50 minimum
- High-ticket items: $100-500 minimum
- Mass market: $10-30 minimum
```

### 5. Regular Monitoring

- Review top-performing codes regularly
- Deactivate underperforming promos
- Monitor usage vs limits to avoid overselling
- Archive completed campaigns

### 6. Backup Your Data

Before major operations, backup MongoDB:
```bash
mongoexport --db promo_codes --collection promotions --out backup.json
```

---

## 🔐 Security Notes

⚠️ **Important:** This is an admin tool with full database access:

1. **Access Control**: Restrict access to authorized administrators only
2. **Audit Trail**: Monitor changes to promotional codes
3. **Database Security**: Secure your MongoDB instance with authentication
4. **Backup**: Keep regular backups of promotion data
5. **Code History**: Consider logging changes to a separate audit collection

### Production Recommendations

For production environments:
- Use MongoDB authentication (username/password)
- Implement role-based access control
- Add audit logging for all modifications
- Use read-only access for reporting
- Run on secured network/VPN

---

## 📊 Sample Usage Session

```
$ python admin_promo_manager.py

[OK] Connected to MongoDB

================================================================================
ADMIN PROMO CODE MANAGEMENT SYSTEM
================================================================================

--------------------------------------------------------------------------------
MAIN MENU
--------------------------------------------------------------------------------
1. View all promo codes
2. View promo code details
3. Add new promo code
4. Edit promo code
5. Delete promo code
6. Reset usage count
0. Exit

Select option (0-6): 1

================================================================================
ALL PROMO CODES
================================================================================

1. Code: SUMMER20
   Discount: 20%
   Campaign: Summer Sale
   Active: True
   ...

Select option (0-6): 3

================================================================================
ADD NEW PROMO CODE
================================================================================

Enter promo code (e.g., SUMMER20): SPRING15
Enter discount percentage (e.g., 20): 15
Enter campaign name (e.g., Summer Sale): Spring Cleaning Sale
Enter description (optional): Get 15% off everything
Enter minimum order value (default 0): 25
Enter maximum uses (leave blank for unlimited): 300
Is this promo code active? (yes/no, default yes): yes
First order only? (yes/no, default no): no

[OK] Promo code 'SPRING15' added successfully!
    Discount: 15%
    Campaign: Spring Cleaning Sale
    First Order Only: False

Select option (0-6): 0

[OK] Exiting admin panel...
[OK] Disconnected from MongoDB
[OK] Admin panel closed
```

---

## 🔗 Related Files

- [README_MONGODB.md](README_MONGODB.md) - MongoDB database setup guide
- [setup_mongodb_data.py](setup_mongodb_data.py) - Initialize sample data
- [show_mongodb_data.py](show_mongodb_data.py) - View promo codes in database
- [order_management_system.py](order_management_system.py) - Main application

---

## 📞 Support & Troubleshooting

### Getting Help

1. Check the **Common Issues** section above
2. Review the **Workflow Examples** for your specific use case
3. Verify MongoDB connection is working
4. Check that PyMongo is installed: `pip list | grep pymongo`

### Debugging Tips

Enable detailed output by adding debug prints:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

---

## 📝 Version Information

| Component | Version |
|-----------|---------|
| Python | 3.7+ |
| PyMongo | 4.0+ |
| MongoDB | 4.0+ |
| Created | March 2026 |
| Updated | March 27, 2026 |

---

## ✨ Key Features Summary

✅ **Easy to Use** - Interactive CLI menu  
✅ **Full CRUD Operations** - Create, Read, Update, Delete promo codes  
✅ **Real-time Updates** - Changes immediately reflected in MongoDB  
✅ **Data Validation** - Input validation and error handling  
✅ **Usage Tracking** - Monitor promo code usage metrics  
✅ **Flexible Rules** - Support for various promotion types and conditions  
✅ **Safe Operations** - Confirmation prompts for destructive actions  
✅ **Detailed Information** - View comprehensive promo code details  

---

**Last Updated:** March 27, 2026  
**Maintained By:** Admin Team  
**Status:** Active & Production Ready
