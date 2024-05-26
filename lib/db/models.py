from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column( Integer(), primary_key=True )
    first_name = Column( String(), nullable=False )
    last_name = Column( String(), nullable=False )
    mobile = Column( String() )

    orders = relationship( "Order", backref=backref("customer") )

    def __repr__(self):
        return (
            f"Customer ID: {self.id}\n"
            f"Name: {self.first_name} {self.last_name}\n"
            f"Mobile: {self.mobile}"
        )


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column( Integer(), primary_key=True )
    item_name = Column( String(), nullable=False )
    price = Column( DECIMAL(4,2), nullable=False )

    def __repr__(self):
        return f"{self.id}: {self.item_name} - ${self.price}"


class Order(Base):
    __tablename__ = "orders"

    id = Column( Integer(), primary_key=True )
    order_date_time = Column( DateTime, nullable=False) 
    customer_id = Column( Integer(), ForeignKey('customers.id') )

    def __repr__(self):
        return (
            f"Order ID: {self.id}\n"
            f"Order Date/Time: {self.order_date_time}\n"
            f"Customer: {self.customer.first_name}\n"
        )
    
class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column( Integer(), primary_key=True )
    order_id = Column( Integer(), ForeignKey("orders.id"), nullable=False )
    menu_item_id = Column( String(), ForeignKey('menu_items.id'), nullable=False )
    quantity = Column( Integer(), nullable=False )

    def __repr__(self):
        return (
            f"Order ID: {self.order_id}\n"
            f"Item Ordered: {self.item_id}\n"
            f"Quantity: {self.quantity}"
        )