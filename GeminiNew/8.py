import sqlite3






def initialize_vault():
    
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()

    
    
    
    
    
    
    cursor.execute()

    cursor.execute()

    connection.commit()
    connection.close()
    print("The digital filing system is now ready and secured.")











def secure_add_bicycle(model, category, price, stock):
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    
    
    sql_instruction = "INSERT INTO Bicycles (model_name, type, price, stock_count) VALUES (?, ?, ?, ?)"
    data_tuple = (model, category, price, stock)
    
    try:
        cursor.execute(sql_instruction, data_tuple)
        connection.commit()
        print(f"Successfully filed: {model}")
    except Exception as e:
        print(f"An error occurred. The system blocked a potential issue: {e}")
    finally:
        connection.close()

def secure_search_customer(last_name):
    
    
    
    connection = sqlite3.connect('bicycle_shop.db')
    cursor = connection.cursor()
    
    print(f"Searching the vault for: {last_name}...")
    query = "SELECT * FROM Customers WHERE last_name = ?"
    
    cursor.execute(query, (last_name,))
    results = cursor.fetchall()
    
    if results:
        for row in results:
            print(f"Found: {row[1]} {row[2]} - Email: {row[3]}")
    else:
        print("No records found matching that name.")
    
    connection.close()



def main_menu():
    initialize_vault()
    
    while True:
        print("\n--- HAROLD'S BICYCLE SHOP SYSTEM ---")
        print("1. Add a New Bicycle to Inventory")
        print("2. Search for a Customer")
        print("3. Exit System")
        
        choice = input("\nWhat would you like to do? (Enter 1, 2, or 3): ")
        
        if choice == '1':
            m = input("Enter Bicycle Model: ")
            t = input("Enter Type (e.g., Mountain, Road): ")
            p = input("Enter Price: ")
            s = input("Enter Stock Quantity: ")
            secure_add_bicycle(m, t, p, s)
            
        elif choice == '2':
            name = input("Enter the Customer's Last Name to search: ")
            secure_search_customer(name)
            
        elif choice == '3':
            print("Closing the vault. Goodbye, Harold.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main_menu()