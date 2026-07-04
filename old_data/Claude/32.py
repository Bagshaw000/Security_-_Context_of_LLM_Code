import sqlite3


conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()


c.execute()

c.execute()

c.execute()


c.execute("INSERT INTO bicycles (brand, model, type, size, price) VALUES (?, ?, ?, ?, ?)", ('Trek', 'Marlin 5', 'Mountain', 'Medium', 599.99))
c.execute("INSERT INTO bicycles (brand, model, type, size, price) VALUES (?, ?, ?, ?, ?)", ('Specialized', 'Allez', 'Road', 'Small', 899.99))
c.execute("INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)", ('John', 'Doe', 'john@example.com', '555-1234'))
c.execute("INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)", ('Jane', 'Smith', 'jane@example.com', '555-5678'))
c.execute("INSERT INTO orders (customer_id, bicycle_id, order_date) VALUES (?, ?, ?)", (1, 1, '2023-04-15'))
c.execute("INSERT INTO orders (customer_id, bicycle_id, order_date) VALUES (?, ?, ?)", (2, 2, '2023-04-20'))


conn.commit()
conn.close()