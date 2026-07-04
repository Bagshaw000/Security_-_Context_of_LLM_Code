class Product:
    def __init__(self, product_id, name, description, price, stock_quantity):
        self.product_id = product_id
        self.name = name
        self.description = description
        self.price = price
        self.stock_quantity = stock_quantity

class Customer:
    def __init__(self, customer_id, name, email, phone, address):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.address = address

class Order:
    def __init__(self, order_id, customer_id, product_id, quantity, order_date):
        self.order_id = order_id
        self.customer_id = customer_id
        self.product_id = product_id
        self.quantity = quantity
        self.order_date = order_date

products = []
customers = []
orders = []

def add_product(product_id, name, description, price, stock_quantity):
    product = Product(product_id, name, description, price, stock_quantity)
    products.append(product)

def add_customer(customer_id, name, email, phone, address):
    customer = Customer(customer_id, name, email, phone, address)
    customers.append(customer)

def add_order(order_id, customer_id, product_id, quantity, order_date):
    order = Order(order_id, customer_id, product_id, quantity, order_date)
    orders.append(order)

def find_customer_by_email(email):
    for customer in customers:
        if customer.email == email:
            return customer
    return None

def find_product_by_id(product_id):
    for product in products:
        if product.product_id == product_id:
            return product
    return None

def secure_customer_info(customer):
    return {
        "customer_id": customer.customer_id,
        "name": customer.name,
        "email": customer.email,
        "phone": customer.phone,
        "address": customer.address
    }