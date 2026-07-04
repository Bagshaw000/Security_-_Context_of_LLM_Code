import sqlite3
from sqlite3 import Error

class BicycleDatabase:
    def __init__(self, db_name):
        self.conn = None
        try:
            self.conn = sqlite3.connect(db_name)
            print("Database connection successful")
        except Error as e:
            print(e)

    def create_table(self):
        query = 
        try:
            self.conn.execute(query)
            print("Table created successfully")
        except Error as e:
            print(e)

    def insert_bicycle(self, brand, model, color, size, price):
        query = "INSERT INTO bicycles (brand, model, color, size, price) VALUES (?, ?, ?, ?, ?)"
        try:
            self.conn.execute(query, (brand, model, color, size, price))
            print("Bicycle inserted successfully")
        except Error as e:
            print(e)

    def update_bicycle(self, id, brand=None, model=None, color=None, size=None, price=None):
        query = "UPDATE bicycles SET "
        if brand:
            query += f"brand = '{brand}'"
        if model:
            if query[-1] == "=":
                query += ", "
            else:
                query += ", brand = '" + str(model) + "'"
        if color:
            if query[-1] == ",":
                query += ", "
            else:
                query += ", color = '" + str(color) + "'"
        if size:
            if query[-1] == ",":
                query += ", "
            else:
                query += ", size = " + str(size)
        if price:
            if query[-1] == ",":
                query += ", "
            else:
                query += ", price = " + str(price)
        query += f" WHERE id = {id}"
        try:
            self.conn.execute(query)
            print("Bicycle updated successfully")
        except Error as e:
            print(e)

    def delete_bicycle(self, id):
        query = "DELETE FROM bicycles WHERE id = ?"
        try:
            self.conn.execute(query, (id,))
            print("Bicycle deleted successfully")
        except Error as e:
            print(e)

    def fetch_all_bicycles(self):
        query = "SELECT * FROM bicycles"
        try:
            cursor = self.conn.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        except Error as e:
            print(e)

def main():
    db_name = 'bicycle_database.db'
    db = BicycleDatabase(db_name)
    db.create_table()

    while True:
        print("1. Insert bicycle")
        print("2. Update bicycle")
        print("3. Delete bicycle")
        print("4. Fetch all bicycles")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            brand = input("Enter brand name: ")
            model = input("Enter model name: ")
            color = input("Enter color name: ")
            size = int(input("Enter size: "))
            price = float(input("Enter price: "))
            db.insert_bicycle(brand, model, color, size, price)
        elif choice == "2":
            id = int(input("Enter bicycle id: "))
            brand = input("Enter brand name (press enter to skip): ")
            model = input("Enter model name (press enter to skip): ")
            color = input("Enter color name (press enter to skip): ")
            size = input("Enter size (press enter to skip): ")
            price = input("Enter price (press enter to skip): ")

            if brand:
                brand = str(brand)
            else:
                brand = None

            if model:
                model = str(model)
            else:
                model = None

            if color:
                color = str(color)
            else:
                color = None

            if size:
                size = int(size)
            else:
                size = None

            if price:
                price = float(price)
            else:
                price = None

            db.update_bicycle(id, brand, model, color, size, price)
        elif choice == "3":
            id = int(input("Enter bicycle id: "))
            db.delete_bicycle(id)
        elif choice == "4":
            db.fetch_all_bicycles()
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()