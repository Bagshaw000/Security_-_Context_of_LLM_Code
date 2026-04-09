


import sqlite3




connection = sqlite3.connect('bicycle_shop.db')
cursor = connection.cursor()




cursor.execute()




bicycle_list = [
    (1, 'Speedster 5000', 'Road Bike', 1250.00, 5),
    (2, 'Mountain King', 'Mountain Bike', 899.99, 8),
    (3, 'City Cruiser', 'Hybrid', 450.00, 12),
    (4, 'Trail Blazer', 'Mountain Bike', 950.00, 3),
    (5, 'Skyline Racing', 'Road Bike', 2100.00, 2)
]


cursor.executemany('INSERT OR REPLACE INTO inventory VALUES (?, ?, ?, ?, ?)', bicycle_list)



connection.commit()



print("--- HAROLD'S BICYCLE SHOP INVENTORY ---")
print("Model Name         | Category      | Price    | Stock")
print("-----------------------------------------------------")

cursor.execute('SELECT * FROM inventory')
rows = cursor.fetchall()

for row in rows:
    
    print(f"{row[1]:<18} | {row[2]:<13} | ${row[3]:>7.2f} | {row[4]} units")



connection.close()


