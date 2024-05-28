from faker import Faker
from faker.providers import BaseProvider
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, MenuItem, Order, OrderDetail
from datetime import datetime
import random

engine = create_engine("sqlite:///data.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()
fake = Faker()

# Delete records from Customer, MenuItem and Order tables
def delete_records():
    session.query(Customer).delete()
    session.query(MenuItem).delete()
    session.query(Order).delete()
    session.query(OrderDetail).delete()

if __name__ == "__main__":
    delete_records()

    # Create and register custom AustralianMobileProvider for seeding in mobile column
    class AustralianMobileProvider(BaseProvider):
            def mobile_number(self):
                return "04" + str(self.random_number(digits=8)).zfill(8)
            
    fake.add_provider(AustralianMobileProvider)

    # Customers
    for i in range (100):
        customer = Customer(
            first_name=fake.first_name(), 
            last_name=fake.last_name(),
            mobile=fake.mobile_number()
            )
        session.add(customer)
        session.commit()


    # Menu Items
    item1 = MenuItem(item_name="Chicken Rice", price=14.90)
    item2 = MenuItem(item_name="Laksa", price=13.90)
    item3 = MenuItem(item_name="Char Kuay Teow", price=15.00)
    item4 = MenuItem(item_name="Nasi Lemak", price=17.90)
    item5 = MenuItem(item_name="Nasi Goreng", price=16.90)
    item6 = MenuItem(item_name="Coke", price=3.00)
    item7 = MenuItem(item_name="Coke Zero", price=3.00)
    item8 = MenuItem(item_name="Sprite", price=3.00)
    item9 = MenuItem(item_name="Fanta", price=3.00)
    item10 = MenuItem(item_name="Mineral Water", price=1.50)

    session.add_all( [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10] )
    session.commit()

    # Orders
    for i in range(100):
        # Define specific start and end dates, then generating a random date/time within the specified range
        start_date = datetime(2024, 5, 1, 0, 0, 0)
        end_date = datetime(2024, 5, 24, 23, 59, 59)
        random_datetime = fake.date_time_between(start_date=start_date, end_date=end_date)

        random_number_customer = random.randint(1, 100) # 100 customers in database
        
        order = Order(
              order_date_time=random_datetime,
              customer_id=random_number_customer
         )

        session.add(order)
        session.commit()

    # Order Details
    unique_order_details = set()

    for i in range (200):

        random_order_id=random.choice(list(range(1, 101)))
        random_menu_item_id=random.choice(list(range(1, 11)))
        random_quantity=random.randint(1,10)

        order_detail_tuple = (random_order_id, random_menu_item_id)

        if order_detail_tuple not in unique_order_details:
            unique_order_details.add(order_detail_tuple)
             
            order_detail = OrderDetail(
                order_id= order_detail_tuple[0],
                menu_item_id= order_detail_tuple[1],
                quantity= random_quantity,
            )

            session.add(order_detail)
            session.commit()
    
    print("Seeding successful for customers data")