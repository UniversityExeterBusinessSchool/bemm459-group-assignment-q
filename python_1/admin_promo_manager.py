"""
Admin Promo Code Management System
Manage promo codes with view, edit, and add functionality
"""

from pymongo import MongoClient
from datetime import datetime
import json

class PromoCodeManager:
    """Manages promo codes in MongoDB"""
    
    def __init__(self):
        """Initialize MongoDB connection"""
        self.mongo_uri = "mongodb://localhost:27017/"
        self.mongo_db_name = "promo_codes"
        self.mongo_collection_name = "promotions"
        
        self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Connect to MongoDB"""
        try:
            self.client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client[self.mongo_db_name]
            self.collection = self.db[self.mongo_collection_name]
            print("[OK] Connected to MongoDB")
            return True
        except Exception as e:
            print(f"[ERROR] Failed to connect to MongoDB: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MongoDB"""
        if self.client:
            self.client.close()
            print("[OK] Disconnected from MongoDB")
    
    def view_all_promos(self):
        """Display all promo codes"""
        try:
            promos = list(self.collection.find({}))
            
            if not promos:
                print("\n[!] No promo codes found")
                return promos
            
            print("\n" + "="*80)
            print("ALL PROMO CODES")
            print("="*80)
            
            for i, promo in enumerate(promos, 1):
                print(f"\n{i}. Code: {promo.get('code', 'N/A')}")
                print(f"   Discount: {promo.get('discount_percent', 0)}%")
                print(f"   Campaign: {promo.get('campaign', 'N/A')}")
                print(f"   Active: {promo.get('active', False)}")
                print(f"   First Order Only: {promo.get('rules', {}).get('first_order_only', False)}")
                print(f"   Type: {promo.get('rules', {}).get('type', 'N/A')}")
                print(f"   Min Order Value: ${promo.get('min_order_value', 0):.2f}")
                print(f"   Max Uses: {promo.get('max_uses', 'Unlimited')}")
                print(f"   Usage Count: {promo.get('usage_count', 0)}")
            
            return promos
            
        except Exception as e:
            print(f"[ERROR] Error fetching promo codes: {e}")
            return []
    
    def view_promo_details(self, code):
        """Display detailed information about a specific promo code"""
        try:
            promo = self.collection.find_one({"code": code.upper()})
            
            if not promo:
                print(f"[ERROR] Promo code '{code}' not found")
                return None
            
            print("\n" + "="*80)
            print(f"PROMO CODE DETAILS: {code.upper()}")
            print("="*80)
            print(f"\nCode: {promo.get('code')}")
            print(f"Discount: {promo.get('discount_percent')}%")
            print(f"Campaign: {promo.get('campaign')}")
            print(f"Description: {promo.get('description', 'N/A')}")
            print(f"Active: {promo.get('active')}")
            print(f"Min Order Value: ${promo.get('min_order_value', 0):.2f}")
            print(f"Max Uses: {promo.get('max_uses', 'Unlimited')}")
            print(f"Current Usage: {promo.get('usage_count', 0)}")
            print(f"\nRules:")
            rules = promo.get('rules', {})
            print(f"  Type: {rules.get('type', 'N/A')}")
            print(f"  First Order Only: {rules.get('first_order_only', False)}")
            print(f"  Exclude Categories: {rules.get('exclude_categories', [])}")
            
            return promo
            
        except Exception as e:
            print(f"[ERROR] Error fetching promo code: {e}")
            return None
    
    def add_promo_code(self):
        """Add a new promo code"""
        try:
            print("\n" + "="*80)
            print("ADD NEW PROMO CODE")
            print("="*80)
            
            # Get input
            code = input("\nEnter promo code (e.g., SUMMER20): ").strip().upper()
            
            # Check if code already exists
            if self.collection.find_one({"code": code}):
                print(f"[ERROR] Promo code '{code}' already exists!")
                return False
            
            discount = float(input("Enter discount percentage (e.g., 20): "))
            campaign = input("Enter campaign name (e.g., Summer Sale): ").strip()
            description = input("Enter description (optional): ").strip()
            
            min_order = float(input("Enter minimum order value (default 0): ") or "0")
            max_uses = input("Enter maximum uses (leave blank for unlimited): ").strip()
            max_uses = int(max_uses) if max_uses else None
            
            active = input("Is this promo code active? (yes/no, default yes): ").strip().lower()
            active = active != 'no'
            
            first_order_only = input("First order only? (yes/no, default no): ").strip().lower()
            first_order_only = first_order_only == 'yes'
            
            # Create promo object
            promo = {
                "code": code,
                "discount_percent": discount,
                "campaign": campaign,
                "description": description if description else None,
                "active": active,
                "min_order_value": min_order,
                "max_uses": max_uses if max_uses else 999999,
                "usage_count": 0,
                "rules": {
                    "type": "percentage_discount",
                    "first_order_only": first_order_only,
                    "exclude_categories": []
                },
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # Insert into MongoDB
            self.collection.insert_one(promo)
            print(f"\n[OK] Promo code '{code}' added successfully!")
            print(f"    Discount: {discount}%")
            print(f"    Campaign: {campaign}")
            print(f"    First Order Only: {first_order_only}")
            
            return True
            
        except ValueError as e:
            print(f"[ERROR] Invalid input: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Error adding promo code: {e}")
            return False
    
    def edit_promo_code(self):
        """Edit an existing promo code"""
        try:
            print("\n" + "="*80)
            print("EDIT PROMO CODE")
            print("="*80)
            
            code = input("\nEnter promo code to edit (e.g., SUMMER20): ").strip().upper()
            
            promo = self.collection.find_one({"code": code})
            if not promo:
                print(f"[ERROR] Promo code '{code}' not found!")
                return False
            
            print(f"\nCurrent details for {code}:")
            print(f"  Discount: {promo.get('discount_percent')}%")
            print(f"  Campaign: {promo.get('campaign')}")
            print(f"  Active: {promo.get('active')}")
            print(f"  Min Order Value: ${promo.get('min_order_value', 0):.2f}")
            print(f"  First Order Only: {promo.get('rules', {}).get('first_order_only', False)}")
            
            print("\n" + "-"*80)
            print("What would you like to edit?")
            print("1. Discount percentage")
            print("2. Campaign name")
            print("3. Description")
            print("4. Active status")
            print("5. Minimum order value")
            print("6. First order only status")
            print("7. Maximum uses")
            print("0. Cancel")
            
            choice = input("\nSelect (0-7): ").strip()
            
            update_data = {"updated_at": datetime.now()}
            
            if choice == "1":
                discount = float(input("Enter new discount percentage: "))
                update_data["discount_percent"] = discount
                
            elif choice == "2":
                campaign = input("Enter new campaign name: ").strip()
                update_data["campaign"] = campaign
                
            elif choice == "3":
                description = input("Enter new description: ").strip()
                update_data["description"] = description
                
            elif choice == "4":
                active = input("Active? (yes/no): ").strip().lower() == 'yes'
                update_data["active"] = active
                
            elif choice == "5":
                min_order = float(input("Enter new minimum order value: "))
                update_data["min_order_value"] = min_order
                
            elif choice == "6":
                first_order = input("First order only? (yes/no): ").strip().lower() == 'yes'
                update_data["rules.first_order_only"] = first_order
                
            elif choice == "7":
                max_uses = input("Enter new maximum uses (blank for unlimited): ").strip()
                max_uses = int(max_uses) if max_uses else 999999
                update_data["max_uses"] = max_uses
                
            elif choice == "0":
                print("[!] Edit cancelled")
                return False
            else:
                print("[ERROR] Invalid choice")
                return False
            
            # Update MongoDB
            self.collection.update_one(
                {"code": code},
                {"$set": update_data}
            )
            
            print(f"\n[OK] Promo code '{code}' updated successfully!")
            return True
            
        except ValueError as e:
            print(f"[ERROR] Invalid input: {e}")
            return False
        except Exception as e:
            print(f"[ERROR] Error editing promo code: {e}")
            return False
    
    def delete_promo_code(self):
        """Delete a promo code"""
        try:
            print("\n" + "="*80)
            print("DELETE PROMO CODE")
            print("="*80)
            
            code = input("\nEnter promo code to delete: ").strip().upper()
            
            promo = self.collection.find_one({"code": code})
            if not promo:
                print(f"[ERROR] Promo code '{code}' not found!")
                return False
            
            # Confirmation
            confirm = input(f"\nAre you sure you want to delete '{code}'? (yes/no): ").strip().lower()
            if confirm != 'yes':
                print("[!] Delete cancelled")
                return False
            
            self.collection.delete_one({"code": code})
            print(f"\n[OK] Promo code '{code}' deleted successfully!")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error deleting promo code: {e}")
            return False
    
    def reset_usage_count(self):
        """Reset usage count for a promo code"""
        try:
            code = input("\nEnter promo code to reset usage: ").strip().upper()
            
            promo = self.collection.find_one({"code": code})
            if not promo:
                print(f"[ERROR] Promo code '{code}' not found!")
                return False
            
            self.collection.update_one(
                {"code": code},
                {"$set": {"usage_count": 0, "updated_at": datetime.now()}}
            )
            
            print(f"\n[OK] Usage count reset for '{code}'")
            return True
            
        except Exception as e:
            print(f"[ERROR] Error resetting usage count: {e}")
            return False


def main():
    """Main admin dashboard"""
    manager = PromoCodeManager()
    
    # Connect to MongoDB
    if not manager.connect():
        return
    
    print("\n" + "="*80)
    print("ADMIN PROMO CODE MANAGEMENT SYSTEM")
    print("="*80)
    
    try:
        while True:
            print("\n" + "-"*80)
            print("MAIN MENU")
            print("-"*80)
            print("1. View all promo codes")
            print("2. View promo code details")
            print("3. Add new promo code")
            print("4. Edit promo code")
            print("5. Delete promo code")
            print("6. Reset usage count")
            print("0. Exit")
            
            choice = input("\nSelect option (0-6): ").strip()
            
            if choice == "1":
                manager.view_all_promos()
                
            elif choice == "2":
                code = input("\nEnter promo code: ").strip()
                manager.view_promo_details(code)
                
            elif choice == "3":
                manager.add_promo_code()
                
            elif choice == "4":
                manager.edit_promo_code()
                
            elif choice == "5":
                manager.delete_promo_code()
                
            elif choice == "6":
                manager.reset_usage_count()
                
            elif choice == "0":
                print("\n[OK] Exiting admin panel...")
                break
            else:
                print("[ERROR] Invalid choice. Please try again.")
                
    except KeyboardInterrupt:
        print("\n\n[!] Admin panel interrupted")
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
    finally:
        manager.disconnect()
        print("[OK] Admin panel closed")


if __name__ == "__main__":
    main()
