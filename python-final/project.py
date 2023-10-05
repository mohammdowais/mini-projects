import os, sys, getpass
from rich.console import Console
from rich.table import Column,Table,box
from finances import manage_finances


def main():
    if check_login():
        clear()
        show_menu()
    else:
        create_account()

def show_menu():
    table = Table(
    "Key",
    "Option",
    title="What you want to do?",
    box=box.ROUNDED
    )
    table.add_row('m','Manage Finances')
    table.add_row('a','Add another User')
    table.add_row('q','Quit')
    console = Console()
    console.print(table)
    key = input("Hit a key in menu:").lower()
    if key == 'm':
        manage_finances()
    else:
        clear()
        print("Se you later!")
    

def check_login():
    user = input("Username: ")
    if user == "hello":
        while True:
            password = getpass.getpass("Password:")
            if password == "1234":
                return True
            else:
                clear()
                print("Incorrect Password")
    else:
        print("User Doesn't Exists.")
        return False

def create_account():
    table = Table("Key","Option",title="Hit the key",box=box.ROUNDED)
    table.add_row("c","Create User")
    table.add_row("q","Quit")
    console = Console()
    console.print(table)
    key = input("Hit a key:")
    if key.lower() == "q":
        sys.exit()
    else:
        print("user Created")
    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def quit():
    sys.exit()

if __name__ == "__main__":
    main()
