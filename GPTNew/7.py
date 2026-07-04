class User:
    def __init__(self, user_id, username, password_hash, email):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.email = email
        self.is_active = True

class Product:
    def __init__(self, product_id, name, description, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity

class Order:
    def __init__(self, order_id, user_id, product_id, quantity, order_date):
        self.order_id = order_id
        self.user_id = user_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date
        self.status = 'Pending'

class Database:
    def __init__(self):
        self.users = {}
        self.products = {}
        self.orders = {}

    def add_user(self, user):
        if user.username not in self.users:
            self.users[user.username] = user

    def add_product(self, product):
        self.products[product.product_id] = product

    def create_order(self, order):
        if order.user_id in self.users and order.product_id in self.products:
            self.orders[order.order_id] = order
            self.products[order.product_id].stock_quantity -= order.quantity

    def authenticate_user(self, username, password_hash):
        user = self.users.get(username)
        if user and user.password_hash == password_hash:
            return user
        return None

    def get_product(self, product_id):
        return self.products.get(product_id)

    def get_user_orders(self, user_id):
        return [order for order in self.orders.values() if order.user_id == user_id]


db = Database()
user = User(1, 'john_doe', 'hashed_password', 'john@example.com')
product = Product(1, 'Mountain Bike', 'A great mountain bike', 299.99, 10)
order = Order(1, 1, 1, 1, '2023-10-01')

db.add_user(user)
db.add_product(product)
db.create_order(order)