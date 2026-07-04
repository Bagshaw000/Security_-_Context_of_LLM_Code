




import sqlite3



connection = sqlite3.connect('BicycleShop.db')
cursor = connection.cursor()






cursor.execute()


cursor.execute()




def add_bicycle(brand, model, price, stock):
    cursor.execute(, (brand, model, price, stock))
    connection.commit() 


add_bicycle('Giant', 'Defy Advanced', 2500.00, 5)
add_bicycle('Trek', 'Domane AL 2', 1100.00, 3)
add_bicycle('Specialized', 'Allez', 1000.00, 8)
add_bicycle('Cannondale', 'Synapse', 1800.00, 4)




def show_inventory():
    print("--- CURRENT BICYCLE INVENTORY ---")
    print("ID | Brand | Model | Price | Stock")
    print("-" * 40)
    
    cursor.execute("SELECT * FROM Bicycles")
    all_bikes = cursor.fetchall()
    
    for bike in all_bikes:
        
        print(f"{bike[0]} | {bike[1]} | {bike[2]} | ${bike[3]} | {bike[4]} left")
    print("-" * 40)




def find_affordable_bikes(max_price):
    print(f"\nSearching for bikes cheaper than ${max_price}:")
    cursor.execute("SELECT Brand, Model, Price FROM Bicycles WHERE Price <= ?", (max_price,))
    results = cursor.fetchall()
    
    if not results:
        print("No bikes found in that price range.")
    for row in results:
        print(f"Option: {row[0]} {row[1]} for ${row[2]}")




show_inventory()
find_affordable_bikes(1500.00)



connection.close()



