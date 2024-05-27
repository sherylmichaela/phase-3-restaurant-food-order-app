from sqlalchemy.orm import declarative_base, relationship, backref
from sqlalchemy import Column, Integer, String, DECIMAL, DateTime, ForeignKey
from sqlalchemy.ext.associationproxy import association_proxy

Base = declarative_base()

class Customer(Base):
    __tablename__ = "customers"

    id = Column( Integer(), primary_key=True )
    first_name = Column( String(), nullable=False )
    last_name = Column( String(), nullable=False )
    mobile = Column( String() )

    # 1-M relationship between Customer and Order
    orders = relationship( "Order", backref=backref("customer") )

    def __repr__(self):
        return (
            f"Customer ID: {self.id}\n"
            f"Name: {self.first_name} {self.last_name}\n"
            f"Mobile: {self.mobile}\n"
        )


class MenuItem(Base):
    __tablename__ = "menu_items"

    id = Column( Integer(), primary_key=True )
    item_name = Column( String(), nullable=False )
    price = Column( DECIMAL(4,2), nullable=False )

    order_details = relationship("OrderDetail", back_populates="menu_item")
    orders = association_proxy("order_details", "order")

    def __repr__(self):
        return f"{self.id}: {self.item_name} - ${self.price}\n"


class Order(Base):
    __tablename__ = "orders"

    id = Column( Integer(), primary_key=True )
    order_date_time = Column( DateTime, nullable=False) 
    customer_id = Column( Integer(), ForeignKey('customers.id') )

    # 1-M relationship between Order and OrderDetail
    order_details = relationship( "OrderDetail", backref=backref("order"))

    menu_items = association_proxy("order_details","menu_item")

    def __repr__(self):
        return (
            f"Order ID: {self.id}\n"
            f"Order Date/Time: {self.order_date_time}\n"
            f"Customer: {self.customer.first_name} {self.customer.last_name}\n"
        )
    
class OrderDetail(Base):
    __tablename__ = "order_details"

    id = Column( Integer(), primary_key=True )
    order_id = Column( Integer(), ForeignKey("orders.id"), nullable=False )
    menu_item_id = Column( Integer(), ForeignKey('menu_items.id'), nullable=False )
    quantity = Column( Integer(), nullable=False )

    menu_item = relationship("MenuItem", back_populates="order_details")
    

    def __repr__(self):
        return (
            f"Order ID: {self.order_id}\n"
            f"Item Ordered: {self.menu_item.item_name}\n"
            f"Quantity: {self.quantity}\n"
        )