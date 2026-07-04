



bicycle_inventory = []



def add_new_bicycle(brand, model, price, quantity):
    
    new_row = {
        "Brand": brand,
        "Model": model,
        "Price": price,
        "Quantity": quantity
    }
    
    bicycle_inventory.append(new_row)



add_new_bicycle("Trek", "Domane", 1500, 5)
add_new_bicycle("Specialized", "Allez", 1100, 3)
add_new_bicycle("Giant", "Defy", 950, 8)
add_new_bicycle("Cannondale", "Synapse", 1300, 4)


def show_all_bikes():
    print("--- CURRENT BICYCLE INVENTORY ---")
    
    for bike in bicycle_inventory:
        print(f"Brand: {bike['Brand']} | Model: {bike['Model']} | Price: ${bike['Price']} | Stock: {bike['Quantity']}")
    print("---------------------------------")


def find_by_brand(search_name):
    print(f"\nSearching for brand: {search_name}...")
    found = False
    for bike in bicycle_inventory:
        if bike["Brand"] == search_name:
            print(f"Result: We have the {bike['Model']} in stock for ${bike['Price']}.")
            found = True
    if not found:
        print("Sorry, we don't carry that brand.")


def calculate_total_value():
    total_value = 0
    for bike in bicycle_inventory:
        
        row_value = bike["Price"] * bike["Quantity"]
        total_value = total_value + row_value
    print(f"\nThe total retail value of your current stock is: ${total_value}")




show_all_bikes()


find_by_brand("Trek")


calculate_total_value()


add_new_bicycle("Brompton", "C Line", 1800, 2)


print("\n--- UPDATED LIST AFTER NEW SHIPMENT ---")
show_all_bikes()