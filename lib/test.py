from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Customer, MenuItem, Order, OrderDetail
# from faker import Faker

engine = create_engine("sqlite:///lib/data.db")
Session = sessionmaker(bind=engine)
session = Session()

# fake = Faker()

if __name__ == "__main__":
    customer1 = session.query(Customer).filter(Customer.id == 1).first()
    customer2 = session.query(Customer).filter(Customer.id == 2).first()

    # Creating order with date, time and customer id

    # order1 = Order(
    #     order_date_time=fake.date_time(),
    #     customer_id=customer1.id,
    # )

    # order2 = Order(
    #     order_date_time=fake.date_time(),
    #     customer_id=customer1.id,
    # )

    # order3 = Order(
    #     order_date_time=fake.date_time(),
    #     customer_id=customer2.id,
    # )

    # Creating orders with ordered items

    # order_detail1 = OrderDetail(
    #     order_id=1,
    #     menu_item_id=2,
    #     quantity=4
    # )

    # order_detail2 = OrderDetail(
    #     order_id=1,
    #     menu_item_id=3,
    #     quantity=1
    # )
    # order_detail3 = OrderDetail(
    #     order_id=2,
    #     menu_item_id=6,
    #     quantity=2
    # )
    # order_detail4 = OrderDetail(
    #     order_id=3,
    #     menu_item_id=8,
    #     quantity=4
    # )


    # session.add_all( [ order_detail1, order_detail2, order_detail3, order_detail4 ] )
    # session.commit()

    ###############################################################################################################

    # FOR TESTING PURPOSES

    # To get all customers
    customers = session.query(Customer).all()
    # for customer in customers:
    #     print(customer)

    # To get all menu items
    menu_items = session.query(MenuItem).all()
    # for item in menu_items:
    #     print(item)

    # To get all orders
    orders = session.query(Order).all()
    # for order in orders:
    #     print(order)

    # To get all order details
    order_details = session.query(OrderDetail).all()
    # for detail in order_details:
    #     print(detail)

    ####################################################################

    # TO GET ALL INFO ABOUT AN ORDER
    order = session.query(Order).filter(Order.id == 1).first()

    # print(order)
    # print(order.customer.first_name)
    # print(order.customer.mobile)
    # print(order.menu_items)
    # print(order.order_details)

    ####################################################################
    
    # TO RETRIEVE ALL ORDERS MADE BY A CUSTOMER

    customer = session.query(Customer).filter(Customer.id == 2).first()
    # for order in customer.orders:
    #     print(order)

    ####################################################################

    # RETRIEVE ITEMS FROM AN ORDER & ADD UP TOTAL
    # customer_order_breakdown = session.query(OrderDetail).filter(OrderDetail.order_id == order_detail1.order_id).all()
    customer_order_breakdown = session.query(OrderDetail).filter(OrderDetail.order_id == 10).all()

    total_price = 0

    # for order in customer_order_breakdown:
    #     item_total = order.menu_item.price * order.quantity
    #     total_price += item_total

    #     print(f"{order.menu_item.item_name:<20} \t${str(order.menu_item.price):<7} \t{order.quantity} \t${str(order.menu_item.price * order.quantity)}")
    # print(f"Total: {str(total_price)}")

    ####################################################################

    # TO GET LAST ORDER PLACED FROM ORDERS TABLE
    last_order = session.query(Order).order_by(Order.id.desc()).first()
    # print(last_order.id)

    ####################################################################

    # TO RETRIEVE ALL ORDERS MADE BY A CUSTOMER USING MOBILE NUMBER
    customer_via_mobile = session.query(Customer).filter(Customer.mobile == "0413689413").first()
    # print(customer_via_mobile)
    # for order in customer_via_mobile.orders:
    #     print(order)
   
    ####################################################################
    
    # TO COMBINE ROWS IN ORDER DETAIL WHICH HAVE THE SAME ORDER ID AND SAME MENU ITEM ORDERED
    same_item_in_same_order = session.query(OrderDetail).filter(OrderDetail.order_id ==  1, OrderDetail.menu_item_id == 1).all()
    
    if len(same_item_in_same_order) > 1:
        first_entry = same_item_in_same_order[0]
        second_entry = same_item_in_same_order[1]
        
        first_entry.quantity += second_entry.quantity

        # session.delete(second_entry)
        # session.commit()
    
    ####################################################################

    

    valid_food_items = {str(i) for i in range(1, 11)}
    # print(valid_food_items)