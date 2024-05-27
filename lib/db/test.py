from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, MenuItem, Order, OrderDetail
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
    )

    order2 = Order(
        order_date_time=fake.date_time(),
        customer_id=customer1.id,
    )

    order3 = Order(
        order_date_time=fake.date_time(),
        customer_id=customer2.id,
    )


    order_detail1 = OrderDetail(
        order_id=1,
        menu_item_id=2,
        quantity=4
    )

    order_detail2 = OrderDetail(
        order_id=1,
        menu_item_id=3,
        quantity=1
    )
    order_detail3 = OrderDetail(
        order_id=2,
        menu_item_id=6,
        quantity=2
    )
    order_detail4 = OrderDetail(
        order_id=3,
        menu_item_id=8,
        quantity=4
    )


    # session.add_all( [ order1, order2, order3, order_detail1, order_detail2, order_detail3, order_detail4 ] )
    # session.commit()

    orders = session.query(Order).all()

    # for order in orders:
    #     print(order)

    order = session.query(Order).filter(Order.id == 1).first()
    # print(order.customer)
    # print(order.menu_items)
    # print(order.order_details)

    # Prints out menu
    menu_items = session.query(MenuItem).all()
    # for item in menu_items:
    #     print(item)

    # Retrieve the orders made by this customer
    customer_orders = session.query(Order).filter(Order.customer_id == customer1.id).all()
    # for order in customer_orders:
    #     print(order.customer)

    # Retrieve the items from an order
    customer_order_breakdown = session.query(OrderDetail).filter(OrderDetail.order_id == order_detail1.order_id).all()
    # for order in customer_order_breakdown:
    #     print(order.menu_item.item_name)


    # print(f"{customer1.first_name}")
    # print(customer1.orders)

    # print(f"{customer2.first_name}")
    # print(customer2.orders)