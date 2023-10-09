import random,os, sys, getpass, pymongo
from rich.console import Console
from rich.table import Column,Table,box
from datetime import datetime
import re
myclient = pymongo.MongoClient("mongodb://localhost:27017/")

db = myclient["budgetdb"]
USERS = db["user"]
TRANSACTIONS = db["transactions"]
LABELS = db["labels"]
console = Console()

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
    get_username = input("Username: ").strip()
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

def manage_finances():
    view_transactions(10)
    show_transaction_menu()
    ...

def show_transaction_menu():
    options = Table("Key","Options",title="Your options",box= box.ROUNDED)
    options.add_row("a","Add Transaction")
    options.add_row("v","View more transactions")
    options.add_row("h","Go Back to Home menu")

    console.print(options)
    choice = input("Hit a key: ").lower()
    
    if choice == 'a':
        add_transaction()
    if choice == 'v':
        view_more_transactions()
    if choice == 'h':
        return 0 

def add_transaction():
    view_labels()
    print("Enter the transaction Details")
    while True:
        try:
            amount = int(input("Enter Amount: ₹"))
        except ValueError:
            print("Amount should be a number")
            continue
        label = input("Select or create a label (purpose): ").lower().title()
        type = "Credit" if input("\n1.'c' for Credit (recived)\n2.'d' debit (spent)\n\nEnter a choice: ") == 'c' else "Debit"
        from_or_to = input("\nPayment made to / Received from: ")
        break
    print(LABELS.find())
    add_label(label)
    transaction = {
        'Amount':amount,
        'Label':label,
        'Type':type,
        'Date':datetime.now().strftime("%Y-%m-%d"),
        'to_or_from':from_or_to
    }
    x  = TRANSACTIONS.insert_one(transaction)
    print(x)
    view_transactions(10)

    

def view_transactions(limit=None,data=None):
    clear()
    transaction_table_view = Table("Amount","Label","Type","Date","Made to",title="Your Payments History",box= box.ROUNDED)
    if not data:
        if not limit:
            data = TRANSACTIONS.find()
        else:
            data = TRANSACTIONS.find().limit(limit)
    for row in data:
        transaction_table_view.add_row(str(row["Amount"]),row["Label"],row["Type"],row["Date"],row["to_or_from"])    
    console.print(transaction_table_view)
    if len(data) == 0:
        print("No Transaction available")
    show_transaction_menu()

def view_more_transactions():
    options = Table("","Amount","Label","Type","Date","Made to",title="Your Payments History",box= box.ROUNDED)
    first_transaction = TRANSACTIONS.find_one({}, sort=[("Date", pymongo.ASCENDING)])
    last_transaction = TRANSACTIONS.find_one({}, sort=[("Date", pymongo.DESCENDING)])
    
    options.add_row("Oldest Transaction",str(first_transaction["Amount"]),first_transaction["Label"],first_transaction["Type"],first_transaction["Date"],first_transaction["to_or_from"])
    options.add_row("Latest Transaction",str(last_transaction["Amount"]),last_transaction["Label"],last_transaction["Type"],last_transaction["Date"],last_transaction["to_or_from"])
    console.print(options)
    first_date = first_transaction["Date"]
    last_date = last_transaction["Date"]
    from_date = get_date("Start",first_date,last_date)
    to_date = get_date("To",first_date,last_date)

    if from_date > to_date:
        from_date, to_date  = to_date, from_date

    query = {"Date": {"$gte": from_date, "$lte": to_date}}
    results = TRANSACTIONS.find(query)
    
    # transaction_table_view = Table("Amount","Label","Type","Date","Made to",title=f"Transaction from {from_date} to {to_date}",box= box.ROUNDED)
    
    # for row in results:        
    #     transaction_table_view.add_row(str(row["Amount"]),row["Label"],row["Type"],row["Date"],row["to_or_from"]) 
    # print()
    # console.print(transaction_table_view)
    # if len(list(results)) == 0:
    #     print("No Transaction available")
    view_transactions(None,list(results))  
    quit()


def get_month():
    months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sept","Oct","Now","Dec"]

    month_table_view = Table()
    for month in months:
        month_table_view.add_column(month)
    month_table_view.add_row("1","2","3","4","5","6","7","8","9","10","11","12")
    
    while True:
        console.print(month_table_view)
        month = input("Enter Month:")
        try:
            month = int(month)
            if month > 12 or month < 0:
                raise ValueError
        except ValueError:
            try:
                month = month.strip().lower().title()[:3]
                month = months.index(month) + 1
            except ValueError:      
                clear()
                print("\n\nPlease ENTER VALID Month")
                continue
        break
    return month

def get_date(type,f_date,l_date):
    
    f_date = datetime.strptime(f_date,"%Y-%m-%d")
    l_date = datetime.strptime(l_date,"%Y-%m-%d")
    while True:
        date = input(f"Enter {type} Date (yyyy-mm-dd):")
        date_pattern = r'\d{4}-\d{2}-\d{2}'        
        if re.match(date_pattern, date):
            if not isinstance(date, datetime):   
                date   = datetime.strptime(date,"%Y-%m-%d")
            if date < f_date:
                print("\nEnter a date after the oldest transaction")
            else:
                return date.strftime("%Y-%m-%d")
        else:
            print(f"\nInvalid date\nValid format:(yyyy-mm-dd)\nExample: 2023-05-01\n")
    

def view_labels():
    labels = LABELS.find()

    label_table_view = Table("Label Name",title="Labels",box = box.ROUNDED)
    for label in labels:
        label_table_view.add_row(label["label"])
    console.print(label_table_view)

def add_label(label):
    LABELS.insert_one({"label":label})
    

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def quit():
    sys.exit()

if __name__ == "__main__":
    # add_transaction()
    view_more_transactions()
    # show_menu()
    # main()
