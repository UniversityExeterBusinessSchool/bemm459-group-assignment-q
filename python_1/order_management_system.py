"""
Polyglot Persistence Application - Order Management System
Demonstrates integration between SQL Server and MongoDB for promo code validation
University of Exeter - BEMM459 Database Technologies for Business Analytics
"""

import pyodbc
from pymongo import MongoClient
from datetime import datetime
import sys


class DatabaseConnection:
    """Handles all database connections and operations"""
    
    def __init__(self):
        """Initialize database connection parameters"""
        # SQL Server Configuration
        self.sql_server = "mcruebs04.isad.isadroot.ex.ac.uk"
        self.sql_database = "BEMM459_2026_Group_Q"
        self.sql_username = "Group_Q_2026"
        self.sql_password = "MrjV827*Wr"
        
        # MongoDB Configuration
        self.mongo_uri = "mongodb://localhost:27017/"
        self.mongo_db = "promo_codes"
        self.mongo_collection = "promotions"
        
        self.sql_connection = None
        self.mongo_client = None
        self.mongo_db_connection = None
        
    def connect_sql_server(self):
        """Establish connection to SQL Server"""
        # Try ODBC Driver 18 first, then fallback to 17
        for driver_version in ["ODBC Driver 18 for SQL Server", "ODBC Driver 17 for SQL Server"]:
            try:
                # Add SSL/TLS encryption settings for mandatory encryption requirement
                connection_string = (
                    f"Driver={{{driver_version}}};"
                    f"Server={self.sql_server};"
                    f"Database={self.sql_database};"
                    f"UID={self.sql_username};"
                    f"PWD={self.sql_password};"
                    f"Encrypt=yes;"  # Enable SSL/TLS encryption
                    f"TrustServerCertificate=yes;"  # Trust the server's certificate
                    f"Connection Timeout=5;"  # 5-second timeout for SSL handshake
                )
                self.sql_connection = pyodbc.connect(connection_string)
                print(f"[OK] Successfully connected to SQL Server (using {driver_version})")
                return True
            except pyodbc.Error as e:
                print(f"    [DEBUG] {driver_version}: {str(e)[:80]}")
                continue
            except Exception as e:
                continue
        
        # If both drivers failed
        print(f"[ERROR] Error connecting to SQL Server")
        print("\nTroubleshooting tips:")
        print("1. Ensure you have ODBC Driver 18 or 17 for SQL Server installed")
        print("2. Server requires Encrypt=yes and TrustServerCertificate=yes")
        print("3. Check your server name, username, and password")
        print("4. Verify your database exists on the server")
        return False
    
    def connect_mongodb(self):
        """Establish connection to MongoDB"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri, serverSelectionTimeoutMS=5000)
            # Test the connection
            self.mongo_client.admin.command('ping')
            self.mongo_db_connection = self.mongo_client[self.mongo_db]
            print("[OK] Successfully connected to MongoDB")
            return True
        except Exception as e:
            print(f"\n[ERROR] Error connecting to MongoDB: {e}")
            import traceback
            traceback.print_exc()
            print("\nTroubleshooting tips:")
            print("1. Ensure MongoDB is running locally on port 27017")
            print("2. Check if MongoDB service is installed and started")
            print("3. On Windows, start MongoDB with: mongod")
            return False
    
    def get_customer_id_by_email(self, email):
        """Get CustomerID from email address"""
        try:
            if not self.sql_connection:
                return None
            
            cursor = self.sql_connection.cursor()
            cursor.execute("SELECT CustomerID FROM Customer WHERE Email = ?", (email,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result[0]
            return None
        except Exception as e:
            print(f"[ERROR] Error fetching customer: {e}")
            return None
    
    def get_customer_order_count(self, customer_id):
        """Get number of orders for a customer"""
        try:
            if not self.sql_connection:
                return 0
            
            cursor = self.sql_connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM Orders WHERE CustomerID = ?", (customer_id,))
            result = cursor.fetchone()
            cursor.close()
            
            if result:
                return result[0]
            return 0
        except Exception as e:
            print(f"[ERROR] Error checking customer orders: {e}")
            return 0
    
    def insert_customer(self, email, name):
        """Create a new customer in SQL Server"""
        try:
            if not self.sql_connection:
                print("[ERROR] SQL Server not connected. Cannot create customer.")
                return None
            
            cursor = self.sql_connection.cursor()
            
            # Get the next CustomerID (PRIMARY KEY, not auto-increment)
            cursor.execute("SELECT ISNULL(MAX(CustomerID), 0) + 1 FROM Customer")
            next_customer_id = cursor.fetchone()[0]
            
            # Insert new customer with explicit CustomerID
            query = """
            INSERT INTO Customer (CustomerID, Name, Email)
            VALUES (?, ?, ?)
            """
            
            cursor.execute(query, (next_customer_id, name, email))
            self.sql_connection.commit()
            cursor.close()
            
            print(f"[OK] New customer created!")
            print(f"    CustomerID: {next_customer_id}")
            print(f"    Name: {name}")
            print(f"    Email: {email}")
            return next_customer_id
            
        except pyodbc.Error as e:
            error_msg = str(e)
            print(f"[ERROR] Failed to create customer: {error_msg[:120]}")
            return None
        except Exception as e:
            print(f"[ERROR] Unexpected error creating customer: {e}")
            return None
    
    def disconnect(self):
        """Close all database connections"""
        if self.sql_connection:
            self.sql_connection.close()
        if self.mongo_client:
            self.mongo_client.close()


class ProductManager:
    """Manages product-related operations"""
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
        self.products = []
        
    def fetch_all_products(self):
        """Fetch all products from SQL Server"""
        if not self.db.sql_connection:
            return False
            
        try:
            cursor = self.db.sql_connection.cursor()
            query = "SELECT ProductID, ProductName, Price FROM Products ORDER BY ProductID"
            cursor.execute(query)
            
            self.products = []
            for row in cursor.fetchall():
                self.products.append({
                    'id': row[0],
                    'name': row[1],
                    'price': row[2]
                })
            
            cursor.close()
            
            if not self.products:
                print("\n[ERROR] No products found in database")
                return False
                
            print(f"[OK] Fetched {len(self.products)} products from database")
            return True
            
        except pyodbc.Error as e:
            print(f"[ERROR] Error fetching products: {e}")
            return False
    
    def display_products(self):
        """Display products in indexed format"""
        if not self.products:
            print("[ERROR] No products available to display")
            return
            
        print("\n" + "="*60)
        print("AVAILABLE PRODUCTS")
        print("="*60)
        
        for index, product in enumerate(self.products, 1):
            print(f"{index}. {product['name']:<40} ${product['price']:.2f}")
        
        print("="*60)


class PromoCodeValidator:
    """Manages promo code validation with MongoDB"""
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
        
    def validate_promo_code(self, code, order_value=0, customer_id=None):
        """
        Validate promo code from MongoDB with comprehensive checks
        
        Args:
            code: Promo code to validate
            order_value: Order value to check against min_order_value
            customer_id: Customer ID for first_order_only validation
        """
        try:
            if self.db.mongo_db_connection is None:
                print("[ERROR] MongoDB not connected")
                return None
            
            collection = self.db.mongo_db_connection[self.db.mongo_collection]
            promo = collection.find_one({"code": code})
            
            if promo is None:
                print(f"[ERROR] Promo code '{code}' not found")
                return None
            
            # Check 1: Is promo code active?
            is_active = promo.get('active')
            if is_active is None or is_active == False:
                print(f"[ERROR] Promo code '{code}' is no longer active")
                return None
            
            # Check 2: Has maximum uses been reached?
            usage_count = promo.get('usage_count', 0)
            max_uses = promo.get('max_uses', 0)
            if usage_count >= max_uses:
                print(f"[ERROR] Promo code '{code}' has reached maximum uses")
                return None
            
            # Check 3: Does order meet minimum order value?
            min_order_value = promo.get('min_order_value', 0)
            if order_value < min_order_value:
                print(f"[ERROR] Order value ${order_value:.2f} is below minimum required ${min_order_value:.2f}")
                return None
            
            # Check 4: Is this a first-order-only promo?
            rules = promo.get('rules', {})
            first_order_only = rules.get('first_order_only', False)
            
            if first_order_only and customer_id:
                order_count = self.db.get_customer_order_count(customer_id)
                if order_count > 0:
                    print(f"[ERROR] Promo code '{code}' is only valid for first-time customers")
                    return None
            
            # All checks passed!
            print(f"[OK] Valid promo code! Discount: {promo.get('discount_percent', 0)}%")
            return promo
            
        except Exception as e:
            print(f"[ERROR] Error validating promo code: {e}")
            return None
    
    def update_usage_count(self, promo_code):
        """Update usage count for promo code"""
        try:
            if self.db.mongo_db_connection is None:
                return False
                
            collection = self.db.mongo_db_connection[self.db.mongo_collection]
            collection.update_one(
                {"code": promo_code},
                {"$inc": {"usage_count": 1}}
            )
            return True
        except Exception as e:
            print(f"[ERROR] Error updating promo code usage: {e}")
            return False


class OrderManager:
    """Manages order creation and storage"""
    
    def __init__(self, db_connection):
        """Initialize with database connection"""
        self.db = db_connection
    
    def create_order(self, customer_id, product_id, product_price, promo_code=None, discount_percent=0):
        """Create a new order in SQL Server"""
        try:
            # Convert Decimal to float if needed (SQL Server returns Decimal type)
            product_price = float(product_price)
            
            # Calculate total amount
            if promo_code:
                discount_amount = product_price * (discount_percent / 100)
                total_amount = product_price - discount_amount
            else:
                total_amount = product_price
            
            # Check if customer_id is valid
            if customer_id is None or customer_id == 0:
                print("[ERROR] Cannot create order - Customer ID is invalid")
                print(f"Debug: customer_id = {customer_id}")
                return False
            
            # Check if SQL Server is connected
            if self.db.sql_connection is None:
                print("[ERROR] SQL Server not connected. Order simulated (not saved).")
                return False
            
            try:
                cursor = self.db.sql_connection.cursor()
                
                # Get the next OrderID (table doesn't use IDENTITY)
                cursor.execute("SELECT ISNULL(MAX(OrderID), 0) + 1 FROM Orders")
                next_order_id = cursor.fetchone()[0]
                
                # Insert order into Orders table with explicit OrderID
                query = """
                INSERT INTO Orders (OrderID, CustomerID, OrderDate, PromoCodeUsed, TotalAmount)
                VALUES (?, ?, ?, ?, ?)
                """
                
                order_date = datetime.now().date()
                cursor.execute(query, (next_order_id, customer_id, order_date, promo_code or None, round(total_amount, 2)))
                self.db.sql_connection.commit()
                
                cursor.close()
                
                print(f"\n[OK] Order created successfully in SQL Server!")
                print(f"  - OrderID: {next_order_id}")
                print(f"  - Order Amount: ${product_price:.2f}")
                if promo_code:
                    discount_amount = product_price * (discount_percent / 100)
                    print(f"  - Discount ({discount_percent}%): -${discount_amount:.2f}")
                print(f"  - Total Amount: ${total_amount:.2f}")
                
                return True
                
            except pyodbc.Error as e:
                # Show the actual SQL error
                error_msg = str(e)
                print(f"\n[ERROR] Failed to save order to SQL Server")
                print(f"Details: {error_msg}")
                print(f"\nTroubleshooting:")
                print(f"1. Verify CustomerID {customer_id} exists in the Customers table")
                print(f"2. Check for foreign key constraints on Orders table")
                print(f"3. Ensure all required fields are valid (OrderDate, TotalAmount, etc.)")
                print(f"\nOrder details that failed to save:")
                print(f"  - OrderID: {next_order_id}")
                print(f"  - CustomerID: {customer_id}")
                print(f"  - OrderDate: {order_date}")
                print(f"  - PromoCodeUsed: {promo_code}")
                print(f"  - TotalAmount: ${total_amount:.2f}")
                return False
            
        except Exception as e:
            print(f"[ERROR] Unexpected error: {e}")
            return False


class InteractiveApplication:
    """Main application controller"""
    
    def __init__(self):
        """Initialize the application"""
        self.db = DatabaseConnection()
        self.product_manager = None
        self.promo_validator = None
        self.order_manager = None
        self.customer_id = None
        self.customer_email = None
        
    def initialize(self):
        """Initialize all connections and managers"""
        print("\n" + "="*60)
        print("ORDER MANAGEMENT SYSTEM - Polyglot Persistence Demo")
        print("="*60)
        print("\nInitializing connections...")
        
        # Connect to SQL Server (optional - can work with MongoDB only)
        sql_connected = self.db.connect_sql_server()
        if not sql_connected:
            print("\n[!] SQL Server unavailable. Running with MongoDB only.")
            print("  (You can install ODBC Driver 18 for full functionality)\n")
        
        # Connect to MongoDB
        if not self.db.connect_mongodb():
            print("\n[ERROR] MongoDB connection failed. Cannot continue.")
            print("Troubleshooting:")
            print("1. Ensure MongoDB is running locally on port 27017")
            print("2. Check if MongoDB service is installed and started")
            print("3. On Windows, start MongoDB with: mongod")
            return False
        
        # Initialize managers
        self.product_manager = ProductManager(self.db)
        self.promo_validator = PromoCodeValidator(self.db)
        self.order_manager = OrderManager(self.db)
        
        # Fetch products (use sample if SQL not available)
        if not self.product_manager.fetch_all_products():
            print("\n[!] Using sample products (SQL Server unavailable)")
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
        
        return True
    
    def get_customer_email(self):
        """Get customer email address and name for registration"""
        while True:
            email = input("\nEnter your email address: ").strip().lower()
            
            if not email:
                print("[ERROR] Email cannot be empty")
                continue
            
            if '@' not in email:
                print("[ERROR] Invalid email format")
                continue
            
            # Get customer ID from email
            customer_id = self.db.get_customer_id_by_email(email)
            
            if customer_id:
                self.customer_id = customer_id
                self.customer_email = email
                print(f"[OK] Customer found! Welcome back")
                return customer_id
            else:
                # For new customers, get their name and create account
                print(f"[!] New customer detected. Creating account...")
                name = input("\nEnter your full name: ").strip()
                
                if not name:
                    print("[ERROR] Name cannot be empty")
                    continue
                
                if len(name) < 2:
                    print("[ERROR] Name must be at least 2 characters")
                    continue
                
                # Try to create customer in SQL Server
                new_customer_id = self.db.insert_customer(email, name)
                
                if new_customer_id:
                    # Successfully created in SQL Server
                    self.customer_id = new_customer_id
                    self.customer_email = email
                    print(f"[OK] Account created successfully!\n")
                    return new_customer_id
                else:
                    # Could not create - continue with None (will fail on order insert)
                    self.customer_email = email
                    self.customer_id = None
                    print(f"[!] Account creation failed. You can still browse, but orders may not save.")
                    print(f"    Proceeding without SQL Server customer creation...\n")
                    return None
    
    def get_product_selection(self):
        """Get product selection from user"""
        while True:
            try:
                selection = input("\nSelect a product (enter number): ").strip()
                
                if selection.lower() == 'q':
                    return None
                
                product_index = int(selection) - 1
                
                if 0 <= product_index < len(self.product_manager.products):
                    return self.product_manager.products[product_index]
                else:
                    print(f"[ERROR] Invalid selection. Please enter a number between 1 and {len(self.product_manager.products)}")
            except ValueError:
                print("[ERROR] Invalid input. Please enter a valid number or 'q' to quit")
    
    def get_promo_code(self):
        """Get promo code from user"""
        promo_code = input("\nEnter promo code (or press Enter to skip): ").strip().upper()
        return promo_code if promo_code else None
    
    def process_order(self, selected_product):
        """Process the complete order workflow"""
        print(f"\n{'='*60}")
        print(f"Product Selected: {selected_product['name']}")
        print(f"Price: ${selected_product['price']:.2f}")
        print(f"{'='*60}")
        
        # Get promo code
        promo_code = self.get_promo_code()
        discount_percent = 0
        
        # Validate promo code if provided
        if promo_code:
            # Validate with comprehensive checks
            promo = self.promo_validator.validate_promo_code(
                code=promo_code,
                order_value=selected_product['price'],
                customer_id=self.customer_id
            )
            if promo:
                discount_percent = promo.get('discount_percent', 0)
                # Update usage in MongoDB
                self.promo_validator.update_usage_count(promo_code)
            else:
                print("Proceeding without promo code...")
                promo_code = None
        
        # Create order
        success = self.order_manager.create_order(
            customer_id=self.customer_id,
            product_id=selected_product['id'],
            product_price=selected_product['price'],
            promo_code=promo_code,
            discount_percent=discount_percent
        )
        
        return success
    
    def run(self):
        """Run the interactive application"""
        if not self.initialize():
            print("\n[ERROR] Failed to initialize application. Exiting...")
            return
        
        print("\n" + "="*60)
        print("WELCOME TO ORDER MANAGEMENT SYSTEM")
        print("="*60)
        
        # Step 1: Get customer email
        self.get_customer_email()
        
        print("\nApplication ready! press 'q' at product selection to exit.\n")
        
        try:
            while True:
                # Display products
                self.product_manager.display_products()
                
                # Get product selection
                selected_product = self.get_product_selection()
                if selected_product is None:
                    break
                
                # Process order
                self.process_order(selected_product)
                
                # Ask if user wants to continue
                continue_choice = input("\nPlace another order? (yes/no): ").strip().lower()
                if continue_choice != 'yes' and continue_choice != 'y':
                    break
        
        except KeyboardInterrupt:
            print("\n\nApplication interrupted by user")
        except Exception as e:
            print(f"\n[ERROR] Unexpected error: {e}")
        finally:
            # Clean up
            print("\nClosing database connections...")
            self.db.disconnect()
            print("[OK] Application closed successfully")


def main():
    """Entry point of the application"""
    app = InteractiveApplication()
    app.run()


if __name__ == "__main__":
    main()
