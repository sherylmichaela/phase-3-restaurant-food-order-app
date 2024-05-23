from faker import Faker
from faker.providers import BaseProvider
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Customer, MenuItem, Order

if __name__ == "__main__":
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

    delete_records()

    # Create and register custom AustralianMobileProvider
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

    print("Seeding successful for customers data")

    # Menu Items



    # Orders
