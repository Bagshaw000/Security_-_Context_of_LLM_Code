import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO bicycles (brand, model, price, quantity) VALUES (?, ?, ?, ?)", ("Trek", "Emonda SLR 6", 3499.99, 10))
c.execute("INSERT INTO bicycles (brand, model, price, quantity) VALUES (?, ?, ?, ?)", ("Specialized", "Roubaix Expert", 4199.99, 8))
c.execute("INSERT INTO bicycles (brand, model, price, quantity) VALUES (?, ?, ?, ?)", ("Giant", "Defy Advanced 1", 2299.99, 15))

c.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)", ("John Doe", "jdoe@example.com", "123 Main St, Anytown USA"))
c.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)", ("Jane Smith", "jsmith@example.com", "456 Oak Rd, Somewhere City"))
c.execute("INSERT INTO customers (name, email, address) VALUES (?, ?, ?)", ("Bob Johnson", "bjohnson@example.com", "789 Maple Ave, Other Town"))

c.execute("INSERT INTO orders (customer_id, bicycle_id, quantity, order_date) VALUES (?, ?, ?, ?)", (1, 1, 1, "2023-04-01"))
c.execute("INSERT INTO orders (customer_id, bicycle_id, quantity, order_date) VALUES (?, ?, ?, ?)", (2, 2, 1, "2023-04-15"))
c.execute("INSERT INTO orders (customer_id, bicycle_id, quantity, order_date) VALUES (?, ?, ?, ?)", (3, 3, 2, "2023-05-01"))


conn.commit()
conn.close()