from config import session
from models import Customer, MenuItem, Order, OrderDetail
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

def place_new_order():
    clear()

    print("\nPls enter your first name.")
    first_name = input()
    print("\nPls enter your last name/initial.")
    last_name = input()
    print("\nPlease enter your mobile number.")
    mobile = input()

    # Checks for existing customer. Adds customer if new.

    existing_customer = session.query(Customer).filter_by(first_name=first_name, last_name=last_name, mobile=mobile).first()

    if not existing_customer:
        new_customer = Customer(first_name=first_name, last_name=last_name, mobile=mobile)
        session.add(new_customer)
        session.commit()
        clear()
        print(f"Welcome to Sheryl's Diner, {first_name}. What would you like to order today?\n")
    else:
        clear()
        print(f"Welcome back {first_name}! What would you like to order today?\n")


    # Proceeds to place order

    def get_menu():
        menu_items = session.query(MenuItem).all()

        for item in menu_items:
            print(item)

    header("MENU", "*", 30)
    get_menu()
    print("*" * 30)

    food_item = input()
    print("\nQuantity? (Pls input only numbers.)")

    

    quantity = int( input() )

   
        
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