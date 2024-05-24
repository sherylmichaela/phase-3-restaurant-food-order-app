from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, MenuItem, Order
from faker import Faker

engine = create_engine("sqlite:///data.db")
Session = sessionmaker(bind=engine)
session = Session()

fake = Faker()

if __name__ == "__main__":
    customer1 = session.query(Customer).filter(Customer.id == 1).first()
    customer2 = session.query(Customer).filter(Customer.id == 2).first()

    order1 = Order(
        order_date_time=fake.date_time(),
        customer_id=customer1.id,
        item_id=1,
        quantity=2
    )

    order2 = Order(
        order_date_time=fake.date_time(),
        customer_id=customer1.id,
        item_id=4,
        quantity=1
    )

    order3 = Order(
        order_date_time=fake.date_time(),
        customer_id=customer2.id,
        item_id=5,
        quantity=1
    )

    session.add_all( [ order1, order2, order3 ] )
    session.commit()

    print(f"{customer1.first_name}")
    print(customer1.orders)

    print(f"{customer2.first_name}")
    print(customer2.orders)