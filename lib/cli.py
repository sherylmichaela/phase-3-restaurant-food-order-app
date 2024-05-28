from config import session
from models import Customer, MenuItem, Order, OrderDetail
from colorama import Back, Fore, Style
import os

def clear():
    if os.name == "posix":
        os.system("clear")
    else:
        os.system("cls")

def header(title, symbol, repetition):
    print(symbol * repetition)
    print(title)
    print(symbol * repetition)

def greet():
    clear()
    header("Welcome to Sheryl's Diner! Pls select an option to get started:", "*", 64)

def main_menu():
    print(Back.CYAN + "  1  " + Style.RESET_ALL + "\tPlace a new order")
    print(Back.GREEN + "  2  " + Style.RESET_ALL + "\tView past orders")
    print(Back.RED + "  0  " + Style.RESET_ALL + "\tExit this program")
    print("=" * 64)

def start():
    start_loop = True

    while start_loop:
        main_menu()

        option_loop = True

        while option_loop:
            choice = int( input() )

            if choice == 1:
                # option_loop = False
                pass
            elif choice == 2:
                # option_loop = False
                pass
            elif choice == 0:
                option_loop = False
                start_loop = False
            else:
                print(Fore.RED + "Invalid input!" + Style.RESET_ALL)

    print(Back.CYAN + "Thank you for choosing Sheryl's Diner. See you soon!" + Style.RESET_ALL)

if __name__ == "__main__":
    greet()
    start()