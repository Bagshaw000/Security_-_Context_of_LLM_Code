import sqlite3


connection = sqlite3.connect('bicycle_shop.db')
cursor = connection.cursor()


cursor.execute('DROP TABLE IF EXISTS inventory')


cursor.execute()



bicycles_to_add = [
    ('The Trail Blazer', 'Mountain', 899.99, 12),
    ('Urban Glide', 'City', 450.00, 25),
    ('Speed Demon', 'Road', 1200.50, 7),
    ('Sky High BMX', 'Stunt', 320.00, 15),
    ('Classic Cruiser', 'Vintage', 550.00, 4)
]


cursor.executemany('INSERT INTO inventory VALUES (?, ?, ?, ?)', bicycles_to_add)


connection.commit()


print("--- HAROLD'S BICYCLE SHOP INVENTORY ---")
cursor.execute('SELECT * FROM inventory')
all_items = cursor.fetchall()

for item in all_items:
    print(f"Bicycle: {item[0]}")
    print(f"Type:    {item[1]}")
    print(f"Price:   ${item[2]}")
    print(f"Stock:   {item[3]} units")
    print("-" * 30)


connection.close()