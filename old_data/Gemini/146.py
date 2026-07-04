




customer_accounts = {
    "Harold Smith": {"pin": "1234", "balance": 1250.50},
    "Sarah Jenkins": {"pin": "5555", "balance": 3400.00},
    "Alice Cooper": {"pin": "9876", "balance": 50.25}
}

def start_atm_system():
    
    while True:
        print("\n--- WELCOME TO THE ATM NETWORK ---")
        print("To turn off the machine, type 'shutdown' as the name.")
        
        name_input = input("Please enter your Full Name: ")

        
        if name_input.lower() == "shutdown":
            print("System shutting down. Goodbye.")
            break

        
        if name_input in customer_accounts:
            pin_input = input("Please enter your 4-digit PIN: ")

            
            if pin_input == customer_accounts[name_input]["pin"]:
                print(f"Access Granted. Welcome, {name_input}.")
                run_transaction_menu(name_input)
            else:
                print("Access Denied: Incorrect PIN.")
        else:
            print("Access Denied: Customer name not found.")

def run_transaction_menu(customer_name):
    
    is_logged_in = True

    while is_logged_in:
        print("\nWhat would you like to do today?")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Log Out")

        selection = input("Enter the number of your choice (1-4): ")

        if selection == "1":
            
            current_balance = customer_accounts[customer_name]["balance"]
            print(f"Your current balance is: ${current_balance:,.2f}")

        elif selection == "2":
            
            deposit_amount = input("How much would you like to deposit? $")
            
            customer_accounts[customer_name]["balance"] += float(deposit_amount)
            new_balance = customer_accounts[customer_name]["balance"]
            print(f"Success! Your new balance is: ${new_balance:,.2f}")

        elif selection == "3":
            
            withdraw_amount = input("How much would you like to withdraw? $")
            withdraw_number = float(withdraw_amount)

            
            if withdraw_number <= customer_accounts[customer_name]["balance"]:
                customer_accounts[customer_name]["balance"] -= withdraw_number
                new_balance = customer_accounts[customer_name]["balance"]
                print(f"Please take your cash. Your new balance is: ${new_balance:,.2f}")
            else:
                print("Transaction Declined: Insufficient funds.")

        elif selection == "4":
            
            print("Logging you out. Please remember to take your card.")
            is_logged_in = False
        
        else:
            print("Invalid choice. Please type 1, 2, 3, or 4.")


start_atm_system()