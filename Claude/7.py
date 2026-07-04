class Bicycle:
    def __init__(self, model, brand, size, color, price):
        self.model = model
        self.brand = brand
        self.size = size
        self.color = color
        self.price = price

class Customer:
    def __init__(self, name, email, phone, address):
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class Order:
    def __init__(self, customer, bicycle, quantity, order_date, delivery_date):
        self.customer = customer
        self.bicycle = bicycle
        self.quantity = quantity
        self.order_date = order_date
        self.delivery_date = delivery_date

class BicycleShop:
    def __init__(self):
        self.bicycles = []
        self.customers = []
        self.orders = []

    def add_bicycle(self, bicycle):
        self.bicycles.append(bicycle)

    def add_customer(self, customer):
        self.customers.append(customer)

    def place_order(self, order):
        self.orders.append(order)

    def get_bicycle_by_model(self, model):
        return [b for b in self.bicycles if b.model == model]

    def get_customer_by_name(self, name):
        return [c for c in self.customers if c.name == name]

    def get_orders_by_customer(self, customer):
        return [o for o in self.orders if o.customer == customer]