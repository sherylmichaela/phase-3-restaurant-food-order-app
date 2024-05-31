from config import session
from models import Customer, MenuItem, Order, OrderDetail
from datetime import datetime
from colorama import Back, Fore, Style
import os

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

###############################################################################################################

check_customer_runs_once = False

def check_customer():
    global check_customer_runs_once
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
                    
                    add_order_id = Order(
                        order_date_time = datetime.now(),
                        customer_id = new_customer.id
                    )

                    session.add(add_order_id)
                    session.commit()

                    loop = False

                    global newly_added_customer
                    newly_added_customer = session.query(Customer).filter_by(first_name=first_name, last_name=last_name, mobile=mobile).first()
                    
                    global logged_customer
                    logged_customer = newly_added_customer


                else:
                    check_customer_runs_once = True

                    add_order_id = Order(
                        order_date_time = datetime.now(),
                        customer_id = customer.id
                    )

                    session.add(add_order_id)
                    session.commit()

                    loop = False

                    logged_customer = customer
            
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
    
###############################################################################################################
# MAIN CODES HERE

def place_orders():

    def get_menu():
        menu_items = session.query(MenuItem).all()
        for item in menu_items:
            print(item)

    check_customer()

    clear()

    while True:

        if logged_customer == customer:
            print(Back.LIGHTGREEN_EX + f"Welcome back {logged_customer.first_name}!" + "\n" + Style.RESET_ALL)
        else:
            print(Back.LIGHTYELLOW_EX + f"Welcome to Sheryl's Makan Place, {logged_customer.first_name}." + "\n" + Style.RESET_ALL)

        header("MENU", "*", 31)
        get_menu()
        print("*" * 31)
        print("\nWhat would you like to order today? Please type in the numerical value of the food/drink item.\nTo go back to the main menu, type 'back'.")
        
        choice = input().strip().lower()
        valid_food_items = {str(i) for i in range(1, 11)}

        if choice == 'back':
            break

        elif choice in valid_food_items:

            while True:
                print("Quantity? (Pls input only numbers.)")

                quantity = input()

                if quantity.isdigit() and 1 <= int(quantity) <= 99:
                    break
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            last_order = session.query(Order).order_by(Order.id.desc()).first()

            add_order_entry = OrderDetail(
                order_id = last_order.id,
                menu_item_id = int(choice),
                quantity = int(quantity)
            )

            session.add(add_order_entry)
            session.commit()


            print("\nItem added to order! Pls select an option below:")
            print(Back.LIGHTCYAN_EX + " 1 " + Style.RESET_ALL + "\tPlace more orders")
            print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView/Modify order & Checkout")
            print("=" * 70)

            choice_after_order_added = input()

            while True:
                if choice_after_order_added == "1":
                    clear()
                    break
                elif choice_after_order_added == "2":
                    pass
                else:
                    print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
                
def view_past_orders():

    print("\nPlease enter your 10-digit mobile number. (i.e. 04xxxxxxxx)")
    mobile = input()
    # mobile = "0413689413"

    customer_found = session.query(Customer).filter(Customer.mobile == mobile).first()
    order_found = session.query(Order).filter()

    if customer_found:
        print(f"\n{customer_found}")
    else:
        print(f"Oops, no orders found.\n")

def remove_null_order():
    
    session.query(Order).filter(Order.order_details == None).delete()
    session.commit()

###############################################################################################################

def start():
    start_loop = True

    while start_loop:
        main_menu()

        while True:
            choice = input()

            if choice == "1": # Place a new order
                clear()
                place_orders()
                break
            elif choice == "2": # View past orders
                clear()
                # view_past_orders()
                break
            elif choice == "0": # Exit this program
                clear()
                start_loop = False
                remove_null_order()
                break
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)
    
    print(Back.BLUE + "Thank you for choosing Sheryl's Makan Place. See you soon!" + Style.RESET_ALL)

if __name__ == "__main__":
    start()