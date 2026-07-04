



inventory = [
    {"Brand": "Trek", "Model": "Domane", "Price": 1200, "Quantity": 5},
    {"Brand": "Giant", "Model": "Defy", "Price": 1100, "Quantity": 3},
    {"Brand": "Specialized", "Model": "Allez", "Price": 1000, "Quantity": 8}
]

def show_inventory():
    
    print("\n--- CURRENT BICYCLE INVENTORY ---")
    
    for bike in inventory:
        print(f"Brand: {bike['Brand']} | Model: {bike['Model']} | Price: ${bike['Price']} | In Stock: {bike['Quantity']}")
    print("----------------------------------")

def add_bike():
    
    print("\n--- ADD A NEW BICYCLE ---")
    brand = input("What is the brand name? ")
    model = input("What is the model name? ")
    price = input("What is the price? ")
    stock = input("How many do you have in the shop? ")

    
    new_bike = {
        "Brand": brand,
        "Model": model,
        "Price": price,
        "Quantity": stock
    }

    
    inventory.append(new_bike)
    print(f"Successfully added the {brand} {model} to your database.")

def search_bike():
    
    search_name = input("\nWhich brand are you looking for? ")
    found = False
    for bike in inventory:
        if bike["Brand"].lower() == search_name.lower():
            print(f"Found: {bike['Brand']} {bike['Model']} - Price: ${bike['Price']}")
            found = True
    if not found:
        print("Sorry, we don't have that brand in the database.")


while True:
    print("\nBICYCLE SHOP DATABASE SYSTEM")
    print("1. View all bicycles in stock")
    print("2. Add a new bicycle to the list")
    print("3. Search for a brand")
    print("4. Close the program")
    
    choice = input("\nWhat would you like to do? (Type 1, 2, 3, or 4): ")

    if choice == "1":
        show_inventory()
    elif choice == "2":
        add_bike()
    elif choice == "3":
        search_bike()
    elif choice == "4":
        print("Closing the database. Have a great day, Harold!")
        break
    else:
        print("That wasn't a valid option. Please try typing 1, 2, 3, or 4.")