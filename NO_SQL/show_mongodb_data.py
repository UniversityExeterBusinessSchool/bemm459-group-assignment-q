from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['promo_codes']
collection = db['promotions']

# Show available promo codes
print('=' * 70)
print('MONGODB PROMO CODE DATABASE - CURRENT DATA')
print('=' * 70)

count = collection.count_documents({})
print(f'\nTotal promo codes in database: {count}\n')

# Display each promo code
promos = list(collection.find({}, {'code': 1, 'discount_percent': 1, 'active': 1, 'expiry_date': 1, 'usage_count': 1, 'max_uses': 1}))

if count == 0:
    print("[!] No promo codes found in MongoDB")
    print("Run: NoSQL/mongodb_setup.js to add sample promo codes")
else:
    for i, promo in enumerate(promos, 1):
        code = promo.get('code', 'N/A')
        discount = promo.get('discount_percent', 0)
        active = promo.get('active', False)
        usage = promo.get('usage_count', 0)
        max_use = promo.get('max_uses', 999)
        expiry = promo.get('expiry_date', 'N/A')
        
        print(f'{i}. Code: {code}')
        print(f'   Discount: {discount}%')
        print(f'   Active: {active}')
        print(f'   Usage: {usage}/{max_use} uses')
        print(f'   Expires: {expiry}')
        print()

client.close()
