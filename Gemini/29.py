





accounts_database = {
    "Harold": 1250.00,
    "Elizabeth": 3400.50,
    "William": 50.25,
    "Victoria": 10000.00
}

def start_atm_machine():
    
    print("--- Welcome to the English Teachers' Credit Union ATM ---")

    
    user_name = input("Please enter your name to access your account: ")

    
    if user_name in accounts_database:
        print("Login Successful. Hello, " + user_name + "!")

        
        is_finished = False
        while is_finished == False:
            print("\n--- TRANSACTION MENU ---")
            print("1. Check my balance")
            print("2. Put money in (Deposit)")
            print("3. Take money out (Withdraw)")
            print("4. Finish and Exit")

            
            choice = input("What would you like to do? (Type 1, 2, 3, or 4): ")

            if choice == "1":
                
                current_balance = accounts_database[user_name]
                print("Your current balance is: $" + str(current_balance))

            elif choice == "2":
                
                deposit_input = input("How much would you like to deposit? $")
                deposit_amount = float(deposit_input)
                
                
                accounts_database[user_name] = accounts_database[user_name] + deposit_amount
                print("Update complete. Your new balance is: $" + str(accounts_database[user_name]))

            elif choice == "3":
                
                withdraw_input = input("How much would you like to withdraw? $")
                withdraw_amount = float(withdraw_input)

                
                if withdraw_amount <= accounts_database[user_name]:
                    
                    accounts_database[user_name] = accounts_database[user_name] - withdraw_amount
                    print("Please take your cash. Your remaining balance is: $" + str(accounts_database[user_name]))
                else:
                    
                    print("Declined: You do not have enough funds for that amount.")

            elif choice == "4":
                
                print("Thank you for using the ATM. Please take your card. Goodbye!")
                is_finished = True

            else:
                
                print("That was not a valid choice. Please try again.")
    else:
        
        print("Error: We could not find an account under that name.")


start_atm_machine()