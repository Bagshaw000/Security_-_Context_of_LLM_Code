





bank_ledger = {
    "Alice": {"pin": "1234", "balance": 1000.00},
    "Bob": {"pin": "5678", "balance": 500.50},
    "Charlie": {"pin": "0000", "balance": 25.00}
}


def run_atm_machine():
    print("--- Welcome to the Neighborhood Bank ATM ---")
    
    
    user_name = input("Please enter your name: ")
    
    
    if user_name in bank_ledger:
        
        entered_pin = input("Please enter your 4-digit secret PIN: ")
        
        
        if entered_pin == bank_ledger[user_name]["pin"]:
            print("Hello, " + user_name + "! Access granted.")
            
            
            stay_logged_in = True
            while stay_logged_in:
                print("\nWhat would you like to do?")
                print("1. Check Balance (See how much money is in the account)")
                print("2. Deposit (Put money into the account)")
                print("3. Withdraw (Take money out of the account)")
                print("4. Exit (Finished for today)")
                
                choice = input("Enter the number of your choice (1-4): ")
                
                if choice == "1":
                    
                    current_balance = bank_ledger[user_name]["balance"]
                    print("Your current balance is: $" + str(current_balance))
                    
                elif choice == "2":
                    
                    deposit_amount = float(input("How much money are you depositing? "))
                    
                    bank_ledger[user_name]["balance"] += deposit_amount
                    print("Success! Your new balance is: $" + str(bank_ledger[user_name]["balance"]))
                    
                elif choice == "3":
                    
                    withdraw_amount = float(input("How much money would you like to take out? "))
                    
                    if withdraw_amount <= bank_ledger[user_name]["balance"]:
                        
                        bank_ledger[user_name]["balance"] -= withdraw_amount
                        print("Please take your cash. Your new balance is: $" + str(bank_ledger[user_name]["balance"]))
                    else:
                        print("Error: You do not have enough money in your account for that.")
                        
                elif choice == "4":
                    
                    print("Thank you for banking with us. Have a wonderful day!")
                    stay_logged_in = False
                else:
                    print("That was not a valid option. Please try again.")
        else:
            
            print("Incorrect PIN. For security, we cannot let you in.")
    else:
        
        print("We're sorry, we couldn't find a bank account under that name.")


run_atm_machine()