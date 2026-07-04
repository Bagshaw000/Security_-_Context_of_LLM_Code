import sqlite3
import re
import getpass
from datetime import datetime

def create_database():
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    cursor.execute()
    
    cursor.execute()
    
    cursor.execute()
    
    connection.commit()
    connection.close()

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_price(price):
    try:
        price_float = float(price)
        return price_float > 0
    except ValueError:
        return False

def validate_phone(phone):
    phone_digits = ''.join(c for c in phone if c.isdigit())
    return len(phone_digits) >= 10

def add_bicycle(model, price, quantity):
    if not validate_price(price):
        print("Error: Price must be a positive number.")
        return False
    
    if quantity <= 0 or not str(quantity).isdigit():
        print("Error: Quantity must be a positive whole number.")
        return False
    
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute(, (model, float(price), int(quantity), datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        print(f"Bicycle '{model}' added successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: A bicycle with model '{model}' already exists.")
        return False
    finally:
        connection.close()

def add_customer(name, email, address, phone):
    if not validate_email(email):
        print("Error: Email format is invalid. Please use format: name@example.com")
        return False
    
    if not validate_phone(phone):
        print("Error: Phone number must have at least 10 digits.")
        return False
    
    if not name or not address:
        print("Error: Name and address cannot be empty.")
        return False
    
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    try:
        cursor.execute(, (name, email, address, phone, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        connection.commit()
        print(f"Customer '{name}' added successfully.")
        return True
    except sqlite3.IntegrityError:
        print(f"Error: A customer with email '{email}' already exists.")
        return False
    finally:
        connection.close()

def view_bicycles():
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id, model, price, quantity FROM bicycles')
    bicycles = cursor.fetchall()
    connection.close()
    
    if not bicycles:
        print("No bicycles in the system.")
        return
    
    print("\n--- BICYCLE INVENTORY ---")
    print(f"{'ID':<5} {'Model':<30} {'Price':<10} {'Quantity':<10}")
    print("-" * 55)
    for bicycle in bicycles:
        print(f"{bicycle[0]:<5} {bicycle[1]:<30} ${bicycle[2]:<9.2f} {bicycle[3]:<10}")
    print()

def view_customers():
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT id, name, email, phone FROM customers')
    customers = cursor.fetchall()
    connection.close()
    
    if not customers:
        print("No customers in the system.")
        return
    
    print("\n--- CUSTOMER LIST ---")
    print(f"{'ID':<5} {'Name':<20} {'Email':<30} {'Phone':<15}")
    print("-" * 70)
    for customer in customers:
        print(f"{customer[0]:<5} {customer[1]:<20} {customer[2]:<30} {customer[3]:<15}")
    print()

def create_order(customer_id, bicycle_id, quantity):
    if quantity <= 0 or not str(quantity).isdigit():
        print("Error: Quantity must be a positive whole number.")
        return False
    
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    cursor.execute('SELECT price, quantity FROM bicycles WHERE id = ?', (bicycle_id,))
    bicycle = cursor.fetchone()
    
    if not bicycle:
        print("Error: Bicycle not found.")
        connection.close()
        return False
    
    bike_price, available_quantity = bicycle
    
    if quantity > available_quantity:
        print(f"Error: Only {available_quantity} bicycles in stock.")
        connection.close()
        return False
    
    cursor.execute('SELECT id FROM customers WHERE id = ?', (customer_id,))
    if not cursor.fetchone():
        print("Error: Customer not found.")
        connection.close()
        return False
    
    total_price = bike_price * quantity
    
    try:
        cursor.execute(, (customer_id, bicycle_id, quantity, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), total_price))
        
        cursor.execute(, (quantity, bicycle_id))
        
        connection.commit()
        print(f"Order created successfully. Total: ${total_price:.2f}")
        return True
    except Exception as e:
        print(f"Error creating order: {str(e)}")
        return False
    finally:
        connection.close()

def view_orders():
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    cursor.execute()
    orders = cursor.fetchall()
    connection.close()
    
    if not orders:
        print("No orders in the system.")
        return
    
    print("\n--- ORDER HISTORY ---")
    print(f"{'Order ID':<10} {'Customer':<20} {'Bicycle':<20} {'Qty':<5} {'Date':<20} {'Total':<10}")
    print("-" * 85)
    for order in orders:
        print(f"{order[0]:<10} {order[1]:<20} {order[2]:<20} {order[3]:<5} {order[4]:<20} ${order[5]:<9.2f}")
    print()

def main_menu():
    create_database()
    
    while True:
        print("\n=== BICYCLE SHOP MANAGEMENT SYSTEM ===")
        print("1. Add a new bicycle")
        print("2. Add a new customer")
        print("3. View all bicycles")
        print("4. View all customers")
        print("5. Create an order")
        print("6. View all orders")
        print("7. Exit")
        
        choice = input("\nEnter your choice (1-7): ").strip()
        
        if choice == '1':
            model = input("Enter bicycle model: ").strip()
            price = input("Enter price: ").strip()
            quantity = input("Enter quantity: ").strip()
            add_bicycle(model, price, quantity)
        
        elif choice == '2':
            name = input("Enter customer name: ").strip()
            email = input("Enter customer email: ").strip()
            address = input("Enter customer address: ").strip()
            phone = input("Enter customer phone: ").strip()
            add_customer(name, email, address, phone)
        
        elif choice == '3':
            view_bicycles()
        
        elif choice == '4':
            view_customers()
        
        elif choice == '5':
            view_customers()
            customer_id = input("Enter customer ID: ").strip()
            view_bicycles()
            bicycle_id = input("Enter bicycle ID: ").strip()
            quantity = input("Enter quantity to order: ").strip()
            try:
                create_order(int(customer_id), int(bicycle_id), int(quantity))
            except ValueError:
                print("Error: Please enter valid numbers.")
        
        elif choice == '6':
            view_orders()
        
        elif choice == '7':
            print("Thank you for using the Bicycle Shop Management System. Goodbye!")
            break
        
        else:
            print("Error: Please enter a number between 1 and 7.")

if __name__ == '__main__':
    main_menu()