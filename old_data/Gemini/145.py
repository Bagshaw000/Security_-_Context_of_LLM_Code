




accounts_database = {
    "1001": {"name": "Harold Smith", "pin": "1234", "balance": 1500.00},
    "1002": {"name": "Sarah Jones", "pin": "5678", "balance": 2450.50},
    "1003": {"name": "Robert Brown", "pin": "9012", "balance": 300.25}
}

def verify_customer(account_number, pin_entered):
    
    if account_number in accounts_database:
        
        if accounts_database[account_number]["pin"] == pin_entered:
            return True
    return False

def check_balance(account_number):
    
    amount = accounts_database[account_number]["balance"]
    print(f"Your current balance is: ${amount:,.2f}")

def withdraw_funds(account_number, amount_to_take):
    
    current_balance = accounts_database[account_number]["balance"]
    if amount_to_take > current_balance:
        print("Insufficient funds. You cannot withdraw more than you have.")
    else:
        
        accounts_database[account_number]["balance"] -= amount_to_take
        new_balance = accounts_database[account_number]["balance"]
        print(f"Successfully withdrew ${amount_to_take:,.2f}")
        print(f"Your new balance is: ${new_balance:,.2f}")

def deposit_funds(account_number, amount_to_add):
    
    accounts_database[account_number]["balance"] += amount_to_add
    new_balance = accounts_database[account_number]["balance"]
    print(f"Successfully deposited ${amount_to_add:,.2f}")
    print(f"Your new balance is: ${new_balance:,.2f}")

def run_atm_machine():
    
    print("--- Welcome to the Network Bank ATM System ---")
    
    acc_id = input("Please enter your Account Number: ")
    pin = input("Please enter your 4-digit PIN: ")

    if verify_customer(acc_id, pin):
        customer_name = accounts_database[acc_id]["name"]
        print(f"\nHello, {customer_name}!")
        
        
        keep_going = True
        while keep_going:
            print("\nWhat would you like to do today?")
            print("1. View Balance")
            print("2. Withdraw Money")
            print("3. Deposit Money")
            print("4. Exit and Take Card")
            
            choice = input("Enter choice (1-4): ")
            
            if choice == "1":
                check_balance(acc_id)
            elif choice == "2":
                amount = float(input("How much would you like to withdraw? "))
                withdraw_funds(acc_id, amount)
            elif choice == "3":
                amount = float(input("How much would you like to deposit? "))
                deposit_funds(acc_id, amount)
            elif choice == "4":
                print("Thank you for banking with us. Have a wonderful day!")
                keep_going = False
            else:
                print("Invalid selection. Please choose a number between 1 and 4.")
    else:
        print("Error: The Account Number or PIN you entered is incorrect.")


run_atm_machine()