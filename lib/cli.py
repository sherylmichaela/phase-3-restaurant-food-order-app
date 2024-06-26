from config import session
from models import Customer, MenuItem, Order, OrderDetail
from datetime import datetime
from colorama import Back, Fore, Style
from tabulate import tabulate
import os
import sys

logged_customer = None

def clear(): # For clearing terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def header(title, symbol, repetition): # Header template
    print(symbol * repetition)
    print(title)
    print(symbol * repetition)

def greet():
    clear()
    header("Welcome to Sheryl's Makan Place!", "*", 32)

def main_menu():
    greet()
    print("\nPls select an option below:\n")
    print(Back.LIGHTGREEN_EX + " 1 " + Style.RESET_ALL + "\tPlace a new order")
    print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView past orders")
    print(Back.LIGHTRED_EX + " 0 " + Style.RESET_ALL + "\tExit this program\n")
    print("=" * 32)

def get_menu():
    menu_items = session.query(MenuItem).all()
    for item in menu_items:
        print(item)

def remove_null_order():
    
    session.query(Order).filter(Order.order_details == None).delete()
    session.commit()

def view_current_order():
    current_order_breakdown = session.query(OrderDetail).filter(OrderDetail.order_id == current_order.id).all()

    total_price = 0
    table = []
    table_item_id = 1
    custom_item_id_to_item_name = {}

    for item in current_order_breakdown:
        custom_item_id_to_item_name[table_item_id] = {
            "menu_item_id": item.menu_item_id,
            "name": item.menu_item.item_name,
        }

        item_total = item.menu_item.price * item.quantity
        total_price += item_total
        table.append([table_item_id, item.menu_item.item_name, f"${item.menu_item.price}", item.quantity, f"${item_total}"])
        table_item_id += 1

    print("Order Summary")
    headers = ["ID", "Item Ordered", "Unit Price", "Quantity", "Item Total"]
    table.append(["", "", "", "Total", f"${total_price}"])
    print(tabulate(table, headers, tablefmt="grid"))

    print("\nPls select an option below:")
    print(Back.LIGHTCYAN_EX + " 1 " + Style.RESET_ALL + "\tAdd item")
    print(Back.LIGHTGREEN_EX + " 2 " + Style.RESET_ALL + "\tModify item quantity")
    print(Back.LIGHTBLUE_EX + " 3 " + Style.RESET_ALL + "\tRemove item")
    print(Back.LIGHTRED_EX + " 4 " + Style.RESET_ALL + "\tCancel order")
    print(Back.LIGHTMAGENTA_EX + " 5 " + Style.RESET_ALL + "\tSubmit order")
    print("=" * 70)

    def modify_item():

        loop = True

        while loop:

            print("Which item would you like to modify?")

            try:
                item_id = int(input())
            
                if item_id in custom_item_id_to_item_name.keys():

                    get_item = session.query(OrderDetail).filter(OrderDetail.order_id == current_order.id, OrderDetail.menu_item_id == custom_item_id_to_item_name[item_id]["menu_item_id"]).first()

                    inner_loop = True

                    while inner_loop:
                        print(f"Input new quantity for {get_item.menu_item.item_name}:")

                        try:
                            new_quantity = input()

                            if 1 <= int(new_quantity) <= 99:
                                get_item.quantity = int(new_quantity)
                                session.commit()
                                inner_loop = False
                                loop = False
                                clear()
                                view_current_order()
                                break
                            else:
                                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                        
                        except ValueError:
                            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
            
            except ValueError:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

    def remove_item():

        loop = True

        while loop:
            
            print("Which item would you like to remove?")

            try:
                item_id = int(input())
            
                if item_id in custom_item_id_to_item_name.keys():

                    get_item = session.query(OrderDetail).filter(OrderDetail.order_id == current_order.id, OrderDetail.menu_item_id == custom_item_id_to_item_name[item_id]["menu_item_id"]).first()

                    inner_loop = True

                    while inner_loop:
                        print(f"You're about to remove {get_item.menu_item.item_name} from your order. Are you sure? (y/n)")
                        
                        choice = input().strip().lower()

                        if choice == "y" or choice == "yes":
                            session.query(OrderDetail).filter(OrderDetail.order_id == current_order.id, OrderDetail.menu_item_id == custom_item_id_to_item_name[item_id]["menu_item_id"]).delete()
                            session.commit()
                            inner_loop = False
                            loop = False
                            clear()
                            view_current_order()
                            break
                        elif choice == "n" or choice == "no":
                            inner_loop = False
                            loop = False
                            clear()
                            view_current_order()
                            break
                        else:
                            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                        
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
            
            except ValueError:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

    def confirm_order():
        
        loop = True

        while loop:

            print("Would you like to proceed with your order? (y/n)")
            choice = input().strip().lower()

            if choice == "y" or choice == "yes":

                inner_loop = True

                while inner_loop:
                    clear()
                    print(f"Yay {logged_customer.first_name}, your order has been submitted!")
                    print("To place a new order, type 'new'.")
                    print("To go back to the main menu, type 'main'.")
                    choice = input().strip().lower()

                    if choice == 'new':
                        clear()
                        inner_loop = False
                        loop = False
                        place_initial_order()
                        break
                    elif choice == 'main':
                        inner_loop = False
                        loop = False
                        clear()
                        start()
                        break
                    else:
                        print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            elif choice == "n" or choice == "no":
                loop = False
                clear()
                view_current_order()
                break
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)


    while True:
        choice = input()

        if choice == "1":
            clear()
            place_subsequent_order()
            break
        elif choice == "2":
            modify_item()
            break
        elif choice == "3":
            remove_item()
            break
        elif choice == "4":

            while True:
                
                print("You're about to cancel your order. Would you like to proceed? (y/n)")
                choice = input().strip().lower()

                if choice == 'y' or choice == 'yes':
                    last_order = session.query(Order).order_by(Order.id.desc()).first()
                    session.query(Order).filter(Order.id == last_order.id).delete()
                    session.query(OrderDetail).filter(OrderDetail.order_id == last_order.id).delete()
                    session.commit()
                    clear()
                    start()
                    break
                elif choice == 'n' or choice == 'no':
                    clear()
                    view_current_order()
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            break
        elif choice == "5":
            confirm_order()
            break
        else:
            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

def check_customer():
    global check_customer_runs_once
    check_customer_runs_once = False

    if not check_customer_runs_once:

        loop = True

        while loop:
           
            print("\nPlease enter your 10-digit mobile number. (i.e. 04xxxxxxxx)")
            mobile = input().strip()
            # mobile = "0413689413"

            if len(mobile) == 10 and mobile.isdigit():
                
                global customer
                customer = session.query(Customer).filter(Customer.mobile == mobile).first()

                if not customer:

                    check_customer_runs_once = True
                    
                    print("\nPls enter your first name.")
                    first_name = input() 
                    # first_name = "Sheryl"
                    print("\nPls enter your last name/initial.")
                    last_name = input()
                    # last_name = "Chee"

                    new_customer = Customer(first_name=first_name, last_name=last_name, mobile=mobile)
                    session.add(new_customer)
                    session.commit()

                    loop = False

                    global newly_added_customer
                    newly_added_customer = session.query(Customer).filter_by(first_name=first_name, last_name=last_name, mobile=mobile).first()
                    
                    global logged_customer
                    logged_customer = newly_added_customer


                else:
                    check_customer_runs_once = True

                    loop = False

                    logged_customer = customer
            
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

def place_subsequent_order():

    header("MENU", "*", 31)
    get_menu()
    print("*" * 31)
    print("\nTo add item, please type in the numerical value of the food/drink item.\nOtherwise, type 'view' to view your current order.")

    while True:
        
        choice = input().strip().lower()
        valid_food_items = {str(i) for i in range(1, 11)}

        if choice == 'view':
            clear()
            view_current_order()
            break

        elif choice in valid_food_items:

            while True:
                print("\nQuantity? (Pls input only numbers.)")

                quantity = input()

                if quantity.isdigit() and 1 <= int(quantity) <= 99:
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            add_item = OrderDetail(
                order_id = current_order.id,
                menu_item_id = int(choice),
                quantity = int(quantity)
            )

            session.add(add_item)
            session.commit()
            
            same_item_in_same_order = session.query(OrderDetail).filter(OrderDetail.order_id == current_order.id, OrderDetail.menu_item_id == choice).all()
    
            if len(same_item_in_same_order) > 1:
                first_entry = same_item_in_same_order[0]
                second_entry = same_item_in_same_order[1]
                
                first_entry.quantity += second_entry.quantity

                session.delete(second_entry)
                session.commit()

            print("\nItem added to order! Pls select an option below:")
            print(Back.LIGHTCYAN_EX + " 1 " + Style.RESET_ALL + "\tAdd items")
            print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView/Modify order & Checkout")
            print("=" * 70)

            while True:
                choice_after_order_added = input()

                if choice_after_order_added == "1":
                    clear()
                    place_subsequent_order()
                    break
                elif choice_after_order_added == "2":
                    clear()
                    view_current_order()
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

def place_initial_order():

    check_customer()

    clear()

    add_order_id = Order(
        order_date_time = datetime.now(),
        customer_id = logged_customer.id
    )

    session.add(add_order_id)
    session.commit()

    if logged_customer == customer:
        print(Back.LIGHTGREEN_EX + f"Welcome back {logged_customer.first_name}!" + "\n" + Style.RESET_ALL)
    else:
        print(Back.LIGHTCYAN_EX + f"Welcome to Sheryl's Makan Place, {logged_customer.first_name}." + "\n" + Style.RESET_ALL)

    header("MENU", "*", 31)
    get_menu()
    print("*" * 31)
    print("\nTo place an order, please type in the numerical value of the food/drink item.\nTo go back to the main menu, type 'back'.")

    while True:
        
        choice = input().strip().lower()
        valid_food_items = {str(i) for i in range(1, 11)}

        if choice == 'back':
            remove_null_order()
            break

        elif choice in valid_food_items:

            while True:
                print("\nQuantity? (Pls input only numbers.)")

                quantity = input()

                if quantity.isdigit() and 1 <= int(quantity) <= 99:
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            global current_order
            current_order = session.query(Order).order_by(Order.id.desc()).first()
            add_item = OrderDetail(
                order_id = current_order.id,
                menu_item_id = int(choice),
                quantity = int(quantity)
            )

            session.add(add_item)
            session.commit()

            print("\nItem added to order! Pls select an option below:")
            print(Back.LIGHTCYAN_EX + " 1 " + Style.RESET_ALL + "\tAdd items")
            print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView/Modify order & Checkout")
            print("=" * 70)

            while True:

                choice_after_order_added = input()

                if choice_after_order_added == "1":
                    clear()
                    place_subsequent_order()
                    break
                elif choice_after_order_added == "2":
                    clear()
                    view_current_order()
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
        else:
            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                
def view_past_orders():

    def options_menu():

        print("\nTo place a new order, type 'new'.")
        print("To go back to the main menu, type 'back'.")

        while True:
            choice = input().strip().lower()
            
            if choice == "new":
                clear()
                place_initial_order()
                break
            elif choice == "back":
                clear()
                main_menu()
                break
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
    
    loop = True

    while loop:
        clear()
        print("\nPlease enter your 10-digit mobile number. (i.e. 04xxxxxxxx)")
        mobile = input().strip()
        # mobile = "0413689413"

        global customer_found
        customer_found = session.query(Customer).filter(Customer.mobile == mobile).first()

        if len(mobile) == 10 and mobile.isdigit() and customer_found:

            if len(customer_found.orders) > 0:

                clear()
                print(f"\nHi {customer_found.first_name}, these are your past orders:")

                get_past_orders = session.query(Order).filter(Order.customer_id == customer_found.id).all()
                past_orders_dict = {}
                
                for order in get_past_orders:
                    get_past_order_details = session.query(OrderDetail).filter(OrderDetail.order_id == order.id).all()

                    if order.id not in past_orders_dict:
                        past_orders_dict[order.id] = {
                            "order_date_time": order.order_date_time,
                            "details": [],
                            "price": []
                        }

                    total_price = 0

                    for item in get_past_order_details:
                        individual_item_total_price = item.quantity * item.menu_item.price
                        total_price += individual_item_total_price
                        past_orders_dict[order.id]["details"].append(f"{item.quantity} * {item.menu_item.item_name}")
                        past_orders_dict[order.id]["price"].append(f"{total_price}")

                past_orders_table = []


                for order_id, order_info in past_orders_dict.items():
                    details = "\n".join(order_info["details"])
                    last_element_in_total_price = "{:.2f}".format(float(order_info["price"][-1]))
                    past_orders_table.append([order_id, order_info["order_date_time"], details, f"${last_element_in_total_price}"])
                    
                headers = ["Order ID", "Order Date & Time", "Details", "Total"]
                print(tabulate(past_orders_table, headers, tablefmt="grid"))

                loop = False

                options_menu()
        
            else:
                print(f"Hi {customer_found.first_name}, looks like you haven't placed any orders.")
                loop = False
                options_menu()

        elif len(mobile) == 10 and mobile.isdigit() and not customer_found:
            print("Oops, looks like you haven't placed any orders.")
            options_menu()
            loop = False
        else:
            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

###############################################################################################################

def start():
    start_loop = True

    while start_loop:
        main_menu()

        while True:
            choice = input()

            if choice == "1": # Place a new order
                clear()
                place_initial_order()
                break
            elif choice == "2": # View past orders
                clear()
                view_past_orders()
                break
            elif choice == "0": # Exit this program
                clear()
                start_loop = False
                break
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
    
    print(Back.BLUE + "Thank you for choosing Sheryl's Makan Place. See you soon!" + Style.RESET_ALL)
    sys.exit()

if __name__ == "__main__":
    start()