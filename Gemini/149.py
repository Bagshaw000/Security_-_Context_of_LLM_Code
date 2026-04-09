






bank_accounts = {
    "1001": {"pin": "1234", "balance": 500.00},
    "1002": {"pin": "8888", "balance": 1200.50},
    "1003": {"pin": "0000", "balance": 50.25}
}




def start_atm_system():
    print("--- Welcome to the English Teacher's Bank Network ---")
    
    
    account_id = input("Please enter your Account Number: ")
    
    
    if account_id in bank_accounts:
        pin_attempt = input("Please enter your 4-digit PIN: ")
        
        
        if pin_attempt == bank_accounts[account_id]["pin"]:
            print("Login successful!")
            run_transaction_menu(account_id)
        else:
            print("Incorrect PIN. Access denied.")
    else:
        print("Account number not recognized.")

def run_transaction_menu(account_id):
    
    while True:
        print("\nWhat would you like to do today?")
        print("1. Check Balance")
        print("2. Withdraw Money")
        print("3. Deposit Money")
        print("4. Exit")
        
        choice = input("Enter the number of your choice (1-4): ")
        
        
        if choice == "1":
            current_bal = bank_accounts[account_id]["balance"]
            print(f"Your current balance is: ${current_bal}")
            
        
        elif choice == "2":
            amount = float(input("How much would you like to withdraw? "))
            if amount <= bank_accounts[account_id]["balance"]:
                bank_accounts[account_id]["balance"] -= amount
                print(f"Please take your cash. New balance: ${bank_accounts[account_id]['balance']}")
            else:
                print("Error: You do not have enough money for that withdrawal.")
                
        
        elif choice == "3":
            amount = float(input("How much would you like to deposit? "))
            bank_accounts[account_id]["balance"] += amount
            print(f"Deposit accepted. New balance: ${bank_accounts[account_id]['balance']}")
            
        
        elif choice == "4":
            print("Thank you for using our ATM. Have a wonderful day!")
            break
            
        else:
            print("That is not a valid option. Please try again.")



if __name__ == "__main__":
    start_atm_system()