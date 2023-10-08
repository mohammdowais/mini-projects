from rich.console import Console
from rich.table import Column,Table,box
from datetime import datetime

console = Console()
budget = 0
transactions = []
labels = []
def manage_finances():
    show_menu()
    ...

def show_menu():
    view_transactions()
    options = Table("Key","Options",title="Your options",box= box.ROUNDED)
    options.add_row("a","Add Transaction")
    options.add_row("v","View more transactions")
    options.add_row("h","Go Back to Home menu")

    console.print(options)
    choice = input("Hit a key: ").lower()
    
    if choice == 'a':
        add_transaction()
    if choice == 'v':
        view_transactions()
    if choice == 'h':
        return 0 

def add_transaction():
    view_labels()
    print("Enter the transaction Details")
    while True:
        try:
            amount = int(input("Enter Amount: ₹"))
        except TypeError:
            print("Amount should be a number")
        label = input("Select or create a label (purpose): ")
        type = "Credit" if input("\n1.'c' for Credit (recived)\n2.'d' debit (spent)\n\nEnter a choice: ") == 'c' else "Debit"
        whom = input("\nShop name or person (to whom payment made): ")
        break
    transaction = {
        'Amount':amount,
        'Label':label,
        'Type':type,
        'Date':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'Made to':whom,
    }
    transactions.append(transaction)
    print(transaction)

    
    ...

def view_transactions():

    transaction_table = Table("Amount","Label","Type","Date","Made to",title="Your Payments History",box= box.ROUNDED)
    for row in transactions:
        transaction_table.add_row(str(row["Amount"]),row["Label"],row["Type"],row["Date"],row["Made to"])    
    console.print(transaction_table)
    
def view_labels():
    label_table = Table("key","Label Name",title="Labels",box = box.ROUNDED)
    console.print(label_table)
    ...
    
if __name__ == "__main__":
    manage_finances()
