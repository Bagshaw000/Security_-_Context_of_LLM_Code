class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

class InventoryReport:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def generate_report(self):
        total_revenue = 0
        for product in self.products:
            revenue = product.price * product.quantity
            print(f"Product: {product.name}, Quantity: {product.quantity}, Price: {product.price}")
            print(f"Revenue: ${revenue:.2f}")
            total_revenue += revenue

        average_price_per_product = total_revenue / len(self.products)
        print(f"\nAverage price per product: ${average_price_per_product:.2f}")

class SalesReport:
    def __init__(self):
        self.sales_data = {}

    def add_sale(self, product_name, quantity):
        if product_name in self.sales_data:
            self.sales_data[product_name] += quantity
        else:
            self.sales_data[product_name] = quantity

    def generate_report(self):
        print("\nSales Report:")
        for product_name, quantity in sorted(self.sales_data.items(), key=lambda x: x[1], reverse=True):
            print(f"Product: {product_name}, Quantity Sold: {quantity}")

class AccountingReport:
    def __init__(self):
        self.inventory = InventoryReport()
        self.sales = SalesReport()

    def add_product_to_inventory(self, name, price, quantity):
        product = Product(name, price, quantity)
        self.inventory.add_product(product)

    def make_sale(self, product_name, quantity):
        self.sales.add_sale(product_name, quantity)

    def generate_report(self):
        print("\nAccounting Report:")
        self.inventory.generate_report()
        self.sales.generate_report()


accounting_report = AccountingReport()
accounting_report.add_product_to_inventory("Product A", 10.0, 100)
accounting_report.add_product_to_inventory("Product B", 20.0, 50)
accounting_report.make_sale("Product A", 20)
accounting_report.make_sale("Product B", 30)
accounting_report.generate_report()