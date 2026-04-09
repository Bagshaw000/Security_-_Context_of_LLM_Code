import sqlite3


conn = sqlite3.connect('bicycle_shop.db')


cursor = conn.cursor()


cursor.execute()


cursor.execute()


cursor.execute()


cursor.execute("INSERT INTO Bicycles (Model, Brand, Color, Size, Price) VALUES ('Mountain Bike', 'Trek', 'Blue', 18, 599.99)")
cursor.execute("INSERT INTO Bicycles (Model, Brand, Color, Size, Price) VALUES ('Road Bike', 'Specialized', 'Red', 21, 899.99)")
cursor.execute("INSERT INTO Customers (Name, Email, Phone) VALUES ('John Doe', 'john.doe@example.com', '555-1234')")
cursor.execute("INSERT INTO Customers (Name, Email, Phone) VALUES ('Jane Smith', 'jane.smith@example.com', '555-5678')")
cursor.execute("INSERT INTO Orders (CustomerID, BicycleID, Quantity, OrderDate) VALUES (1, 1, 1, '2023-04-15')")
cursor.execute("INSERT INTO Orders (CustomerID, BicycleID, Quantity, OrderDate) VALUES (2, 2, 1, '2023-04-20')")


conn.commit()
conn.close()