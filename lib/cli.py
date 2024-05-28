from config import session
from models import Customer, MenuItem, Order, OrderDetail
from datetime import datetime
from colorama import Back, Fore, Style
import os

def clear(): # For clearing terminal
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def header(title, symbol, repetition): # Header template
    print(symbol * repetition)
    print(title)
    print(symbol * repetition)

############################################################################################################### 
def check_customer():

    print("\nPls enter your first name.")
    # first_name = input() 
    first_name = "Sheryl"
    print("\nPls enter your last name/initial.")
    # last_name = input()
    last_name = "Chee"
    print("\nPlease enter your mobile number.")
    # mobile = input()
    mobile = "0413689413"

    # Checks for existing customer. Adds customer if new.

    existing_customer = session.query(Customer).filter_by(first_name=first_name, last_name=last_name, mobile=mobile).first()

    if not existing_customer:
        new_customer = Customer(first_name=first_name, last_name=last_name, mobile=mobile)
        session.add(new_customer)
        session.commit()

        newly_added_customer = session.query(Customer).filter_by(first_name=first_name, last_name=last_name, mobile=mobile).first()
        add_order_id = Order(
            order_date_time = datetime.now(),
            customer_id = newly_added_customer.id
        )

        session.add(add_order_id)
        session.commit()

        clear()
        print(Back.LIGHTYELLOW_EX + f"Welcome to Sheryl's Diner, {first_name}.\n" + Style.RESET_ALL)
    else:
        add_order_id = Order(
            order_date_time = datetime.now(),
            customer_id = existing_customer.id
        )

        session.add(add_order_id)
        session.commit()

        clear()
        print(Back.LIGHTGREEN_EX + f"Welcome back {first_name}!\n" + Style.RESET_ALL)

def order_entry():
    
    # Queries menu items and print them

    def get_menu():
        menu_items = session.query(MenuItem).all()

        for item in menu_items:
            print(item)

    header("MENU", "*", 30)
    get_menu()
    print("*" * 30)
    print("\nWhat would you like to order today? Please type in the numerical value of the food/drink item.")

    # Placing order

    loop = True

    while loop:

        food_loop = True

        while food_loop:
            valid_food_items = {str(i) for i in range(1, 11)}
            food_item = input()
            
            if food_item in valid_food_items:
                food_loop = False
            else:
                print(Fore.RED + "Invalid input! Please enter a number between 1 and 10." + Style.RESET_ALL)
                

        quantity_loop = True

        while quantity_loop:
            print("\nQuantity? (Pls input only numbers.)")

            valid_quantity = {str(i) for i in range(1,100)}
            quantity = input()

            if quantity in valid_quantity:
                quantity_loop = False
                loop = False
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

            last_order = session.query(Order).order_by(Order.id.desc()).first()

            add_order_entry = OrderDetail(
                order_id = last_order.id,
                menu_item_id = int(food_item),
                quantity = int(quantity)
            )

            session.add(add_order_entry)
            session.commit()

def order_entry_flow():
    
    order_entry()

    while True:
        print("\nItem added to order! Pls select an option below:")
        print(Back.LIGHTCYAN_EX + " 1 " + Style.RESET_ALL + "\tPlace more orders")
        print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView/Modify order & Checkout")
        print("=" * 70)
        choice = input()

        if choice == "1":
            clear()
            order_entry()
        elif choice == "2":
            break
        else:
            print(Fore.RED + "Invalid input!" + Style.RESET_ALL)


def place_new_order():
    clear()
    check_customer()
    order_entry_flow()
    
############################################################################################################### 

def greet():
    clear()
    header("Welcome to Sheryl's Makan Place! Pls select an option to get started:", "*", 70)

def main_menu():
    print(Back.LIGHTGREEN_EX + " 1 " + Style.RESET_ALL + "\tPlace a new order")
    print(Back.LIGHTBLUE_EX + " 2 " + Style.RESET_ALL + "\tView past orders")
    print(Back.LIGHTRED_EX + " 0 " + Style.RESET_ALL + "\tExit this program")
    print("=" * 70)

def start():
    start_loop = True

    while start_loop:
        main_menu()

        option_loop = True

        while option_loop:
            choice = input()

            if choice == "1":
                option_loop = False
                place_new_order()
            elif choice == "2":
                # option_loop = False
                pass
            elif choice == "0":
                option_loop = False
                start_loop = False
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

    print(Back.BLUE + "Thank you for choosing Sheryl's Diner. See you soon!" + Style.RESET_ALL)

if __name__ == "__main__":
    greet()
    start()