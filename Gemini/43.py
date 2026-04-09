






bicycle_inventory = [
    {"Brand": "Trek", "Model": "Domane", "Price": 1200, "Stock": 5},
    {"Brand": "Giant", "Model": "Defy", "Price": 1100, "Stock": 3},
    {"Brand": "Specialized", "Model": "Allez", "Price": 950, "Stock": 8}
]

def show_all_bikes():
    
    print("\n--- CURRENT BICYCLE INVENTORY ---")
    
    for bike in bicycle_inventory:
        print(f"BRAND: {bike['Brand']} | MODEL: {bike['Model']} | PRICE: ${bike['Price']} | QUANTITY: {bike['Stock']}")
    print("----------------------------------")

def add_bike_to_list():
    
    print("\nAdding a new bike...")
    brand = input("Enter the brand name (e.g., Cannondale): ")
    model = input("Enter the model name (e.g., Synapse): ")
    price = input("Enter the price (numbers only): ")
    stock = input("Enter how many you have in stock (numbers only): ")
    
    
    new_entry = {"Brand": brand, "Model": model, "Price": price, "Stock": stock}
    
    
    bicycle_inventory.append(new_entry)
    print("Success! The bike has been added to your database.")



while True:
    print("\nBICYCLE SHOP MANAGEMENT SYSTEM")
    print("1. View all bicycles in stock")
    print("2. Add a new bicycle to the database")
    print("3. Close the program")
    
    user_choice = input("\nPlease type 1, 2, or 3 and press the Enter key: ")
    
    if user_choice == "1":
        show_all_bikes()
    elif user_choice == "2":
        add_bike_to_list()
    elif user_choice == "3":
        print("Closing the database. Have a wonderful day, Harold!")
        break
    else:
        print("That wasn't a valid option. Please try typing 1, 2, or 3.")