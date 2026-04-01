from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['promo_codes']
collection = db['promotions']

# Sample promo codes
promo_codes = [
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
        "active": True,
        "usage_count": 0,
        "max_uses": 500,
        "created_at": "2025-01-01",
        "rules": {"min_purchase": 30, "max_discount": 500, "stackable": False}
    },
    {
        "_id": "promo_WELCOME10",
        "code": "WELCOME10",
        "discount_percent": 10,
        "brand_id": 1,
        "brand_name": "TechZone",
        "expiry_date": "2025-12-31",
        "channel": "email",
        "campaign": "Welcome New Customers",
        "min_order_value": 20,
        "applicable_product_ids": [1, 2, 3, 4, 5, 6, 7, 8],
        "customer_types": ["new"],
        "active": True,
        "usage_count": 0,
        "max_uses": 1000,
        "created_at": "2025-01-01",
        "rules": {"min_purchase": 20, "max_discount": 200, "stackable": False}
    },
    {
        "_id": "promo_TECH25",
        "code": "TECH25",
        "discount_percent": 25,
        "brand_id": 2,
        "brand_name": "ElectroHub",
        "expiry_date": "2025-04-30",
        "channel": "promotional",
        "campaign": "Tech Accessories Sale",
        "min_order_value": 50,
        "applicable_product_ids": [2, 5, 6, 7],
        "customer_types": ["existing"],
        "active": True,
        "usage_count": 0,
        "max_uses": 300,
        "created_at": "2025-02-01",
        "rules": {"min_purchase": 50, "max_discount": 300, "stackable": False}
    },
    {
        "_id": "promo_FLASH15",
        "code": "FLASH15",
        "discount_percent": 15,
        "brand_id": 3,
        "brand_name": "GadgetWorld",
        "expiry_date": "2025-03-31",
        "channel": "website",
        "campaign": "Flash Sale",
        "min_order_value": 25,
        "applicable_product_ids": [7, 8],
        "customer_types": ["new", "existing"],
        "active": True,
        "usage_count": 0,
        "max_uses": 100,
        "created_at": "2025-03-01",
        "rules": {"min_purchase": 25, "max_discount": 150, "stackable": False}
    }
]

# Insert promo codes
print('=' * 70)
print('LOADING SAMPLE PROMO CODES INTO MONGODB')
print('=' * 70)

try:
    # Clear existing data
    collection.delete_many({})
    print('\nCleared existing promo codes...')
    
    # Insert new promo codes
    result = collection.insert_many(promo_codes)
    print(f'[OK] Successfully inserted {len(result.inserted_ids)} promo codes')
    
    # Create index on code field
    collection.create_index([("code", 1)], unique=True)
    print('[OK] Created index on code field')
    
    # Display inserted codes
    print('\nPromo Codes Loaded:')
    print('-' * 70)
    promos = collection.find({}, {'code': 1, 'discount_percent': 1, 'active': 1})
    for promo in promos:
        code = promo.get('code', 'N/A')
        discount = promo.get('discount_percent', 0)
        active = promo.get('active', False)
        print(f'  [OK] {code:<15} → {discount}% discount (Active: {active})')
    
    print('\n[OK] MongoDB setup complete!')
    print('Ready to use the application.')
    
except Exception as e:
    print(f'[ERROR] Error: {e}')

finally:
    client.close()
