import os
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import unittest

Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    brand = Column(String)
    category = Column(String) 
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)

    def __repr__(self):
        return f"<Product(name='{self.name}', price={self.price}, stock={self.stock_quantity})>"

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    address = Column(String)

    orders = relationship("Order", back_populates="customer")

class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.id'))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="Pending")

    customer = relationship("Customer", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer, nullable=False)
    price_at_purchase = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

class BicycleShopDB:
    def __init__(self, db_url="sqlite:///:memory:"):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def add_product(self, name, brand, category, price, stock):
        session = self.get_session()
        new_product = Product(name=name, brand=brand, category=category, price=price, stock_quantity=stock)
        session.add(new_product)
        session.commit()
        product_id = new_product.id
        session.close()
        return product_id

    def register_customer(self, first_name, last_name, email, address):
        session = self.get_session()
        customer = Customer(first_name=first_name, last_name=last_name, email=email, address=address)
        session.add(customer)
        session.commit()
        customer_id = customer.id
        session.close()
        return customer_id

    def place_order(self, customer_id, items_list):
        
        session = self.get_session()
        try:
            order = Order(customer_id=customer_id)
            session.add(order)
            session.flush()

            for prod_id, qty in items_list:
                product = session.query(Product).filter_by(id=prod_id).first()
                if not product or product.stock_quantity < qty:
                    raise ValueError(f"Insufficient stock for product ID {prod_id}")
                
                item = OrderItem(
                    order_id=order.id,
                    product_id=prod_id,
                    quantity=qty,
                    price_at_purchase=product.price
                )
                product.stock_quantity -= qty
                session.add(item)
            
            session.commit()
            return order.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

class TestBicycleShop(unittest.TestCase):
    def setUp(self):
        self.db = BicycleShopDB("sqlite:///:memory:")

    def test_inventory_management(self):
        pid = self.db.add_product("Specialized Tarmac", "Specialized", "Road", 2500.00, 10)
        session = self.db.get_session()
        product = session.query(Product).get(pid)
        self.assertEqual(product.stock_quantity, 10)
        session.close()

    def test_order_placement_updates_stock(self):
        pid = self.db.add_product("Trek Fuel EX", "Trek", "MTB", 3200.00, 5)
        cid = self.db.register_customer("John", "Doe", "john.doe@bristol.ac.uk", "123 Park St")
        
        self.db.place_order(cid, [(pid, 2)])
        
        session = self.db.get_session()
        product = session.query(Product).get(pid)
        self.assertEqual(product.stock_quantity, 3)
        session.close()

    def test_insufficient_stock_fails(self):
        pid = self.db.add_product("Brompton C Line", "Brompton", "Folding", 1500.00, 1)
        cid = self.db.register_customer("Jane", "Smith", "jane@email.com", "456 High St")
        
        with self.assertRaises(ValueError):
            self.db.place_order(cid, [(pid, 5)])

if __name__ == "__main__":
    
    shop = BicycleShopDB("sqlite:///bicycle_shop.db")
    
    
    p1 = shop.add_product("Canyon Ultimate", "Canyon", "Road", 4500.0, 5)
    p2 = shop.add_product("Santa Cruz Hightower", "Santa Cruz", "MTB", 5800.0, 3)
    
    cust_id = shop.register_customer("Alice", "Engineer", "alice@example.com", "Bristol Science Park")
    
    try:
        order_id = shop.place_order(cust_id, [(p1, 1), (p2, 1)])
        print(f"Order {order_id} placed successfully.")
    except Exception as e:
        print(f"Order failed: {e}")

    
    print("\nRunning unit tests...")
    unittest.main(exit=False)