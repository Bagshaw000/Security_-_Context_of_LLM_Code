import sqlite3


conn = sqlite3.connect('bicycle_shop.db')


cursor = conn.cursor()


cursor.execute()

cursor.execute()

cursor.execute()


cursor.execute("INSERT INTO bicycles (model, brand, size, price) VALUES (?, ?, ?, ?)", ("Mountain Bike", "Trek", 26.0, 799.99))
cursor.execute("INSERT INTO bicycles (model, brand, size, price) VALUES (?, ?, ?, ?)", ("Road Bike", "Specialized", 54.0, 1499.99))
cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", ("John Doe", "johndoe@example.com", "555-1234"))
cursor.execute("INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)", ("Jane Smith", "janesmith@example.com", "555-5678"))
cursor.execute("INSERT INTO orders (customer_id, bicycle_id, order_date) VALUES (?, ?, ?)", (1, 1, "2023-04-15"))
cursor.execute("INSERT INTO orders (customer_id, bicycle_id, order_date) VALUES (?, ?, ?)", (2, 2, "2023-04-20"))


conn.commit()
conn.close()