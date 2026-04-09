

bank_customers = [
    {"name": "Harold", "pin": "1234", "money": 1000.00},
    {"name": "Sarah", "pin": "5678", "money": 2500.50},
    {"name": "James", "pin": "4321", "money": 50.25}
]

def run_atm_system():
    print("--- Welcome to the ATM Network ---")
    
    
    entered_name = input("Please type your name: ")
    entered_pin = input("Please type your 4-digit PIN: ")

    
    current_user = None
    for person in bank_customers:
        if person["name"] == entered_name and person["pin"] == entered_pin:
            current_user = person

    
    if current_user:
        print("\nHello, " + current_user["name"] + "!")
        
        
        while True:
            print("\nWhat would you like to do today?")
            print("1. View how much money I have (Balance)")
            print("2. Put money into the account (Deposit)")
            print("3. Take money out of the account (Withdraw)")
            print("4. Finished / Exit")
            
            choice = input("Please choose 1, 2, 3, or 4: ")

            if choice == "1":
                
                print("You have $" + str(current_user["money"]) + " in your account.")

            elif choice == "2":
                
                amount = input("How much would you like to put in? ")
                current_user["money"] = current_user["money"] + float(amount)
                print("Success! Your new total is $" + str(current_user["money"]))

            elif choice == "3":
                
                amount = input("How much would you like to take out? ")
                amount_number = float(amount)
                
                if amount_number <= current_user["money"]:
                    current_user["money"] = current_user["money"] - amount_number
                    print("Please take your cash. Your remaining total is $" + str(current_user["money"]))
                else:
                    print("Error: You do not have enough money for that request.")

            elif choice == "4":
                
                print("Thank you for using the ATM. Have a wonderful day!")
                break
            else:
                print("That was not a valid choice. Please try again.")
    else:
        
        print("Sorry, we could not find a customer with that name and PIN.")


run_atm_system()