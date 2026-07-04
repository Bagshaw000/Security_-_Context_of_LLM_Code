import sqlite3

conn = sqlite3.connect('bicycle_shop.db')
c = conn.cursor()

c.execute()

c.execute()

c.execute()

def add_bicycle(model, brand, price, stock):
    c.execute("INSERT INTO Bicycles (model, brand, price, stock) VALUES (?, ?, ?, ?)", (model, brand, price, stock))
    conn.commit()

def add_customer(name, email, phone):
    c.execute("INSERT INTO Customers (name, email, phone) VALUES (?, ?, ?)", (name, email, phone))
    conn.commit()

def place_order(customer_id, bicycle_id, quantity, order_date):
    c.execute("INSERT INTO Orders (customer_id, bicycle_id, quantity, order_date) VALUES (?, ?, ?, ?)", (customer_id, bicycle_id, quantity, order_date))
    conn.commit()

def update_bicycle_stock(bicycle_id, new_stock):
    c.execute("UPDATE Bicycles SET stock = ? WHERE id = ?", (new_stock, bicycle_id))
    conn.commit()

def get_bicycle_info(bicycle_id):
    c.execute("SELECT * FROM Bicycles WHERE id = ?", (bicycle_id,))
    return c.fetchone()

def get_customer_info(customer_id):
    c.execute("SELECT * FROM Customers WHERE id = ?", (customer_id,))
    return c.fetchone()

def get_orders_for_customer(customer_id):
    c.execute("SELECT * FROM Orders WHERE customer_id = ?", (customer_id,))
    return c.fetchall()

def get_orders_for_bicycle(bicycle_id):
    c.execute("SELECT * FROM Orders WHERE bicycle_id = ?", (bicycle_id,))
    return c.fetchall()