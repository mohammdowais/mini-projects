import random,os, sys, getpass, pymongo
from rich.console import Console
from rich.table import Column,Table,box
from finances import manage_finances

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["budgetdb"]
USERS = db["user"]
TRANSACTIONS = db["transactions"]
print(db.list_collection_names())
def main():
    if check_login():
        clear()
        show_menu()
    else:
        created = create_account()
        
        if created:
            check_login()
        else:
            quit()

def show_menu():
    table = Table(
    "Key",
    "Option",
    title="What you want to do?",
    box=box.ROUNDED
    )
    table.add_row('m','Manage Finances')
    table.add_row('s','Account Settings')
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
    clear()
    if not USERS.find_one():
        return False

    print("Welcome Back!\nLogin")
    get_username = input("Username: ")
    user = USERS.find_one({"username":get_username})
    if not user:
        print("User Doesn't Exists.")
        exit()
    else:
        password = user["password"]
        # print("password",password)
        attempts = 5
        while True:
            get_password = getpass.getpass("Password:")
            if get_password == password:
                return True
            else:
                clear()
                phrase = ["retry", "attempt again", "give it another shot", "have another go", "take another crack at it", "make a second attempt", "reattempt", "do over", "give it a second try", "start over", "have a redo", "redo", "try one more time", "make another effort"]

                print("Incorrect Password ",random.choice(phrase).title())
            print("Attempts left: ", attempts)
            attempts -= 1
            if(attempts <= 0):
                print("INTRUDER ALERT!! OWNER NOTIFIED\nPHOTO SEND")
                quit()

def create_account():
    table = Table("Key","Option",title="Welcome!",box=box.ROUNDED)
    table.add_row("c","Create User")
    table.add_row("q","Quit")

    console = Console()
    console.print(table)

    key = input("Hit a key:").lower()
    if key != "c":
        sys.exit()
    else:
        username = input("Create Username: ")
        while True:
            password = getpass.getpass("Create Password:")
            confirm = getpass.getpass("Confirm Password:")

            if password == confirm:
                USERS.insert_one({"username":username,"password":password})
                return True
            else:
                clear()
                print("\nCreated password and confirmed password mismatch\n")
                print(f"Username: {username}")

    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def quit():
    sys.exit()

if __name__ == "__main__":
    main()
