





master_ledger = {
    "Alice Smith": {"secret_code": "1234", "money_in_cell": 500.00},
    "Bob Jones": {"secret_code": "5678", "money_in_cell": 250.50},
    "Charlie Brown": {"secret_code": "9012", "money_in_cell": 1000.00}
}

def process_cash_request(person_name, entered_code, withdrawal_amount):
    
    
    if person_name not in master_ledger:
        print("Error: This person is not in our records. Access denied.")
        return

    
    person_data = master_ledger[person_name]
    correct_code = person_data["secret_code"]
    current_balance = person_data["money_in_cell"]

    
    
    if entered_code != correct_code:
        print("Access Denied: The secret code is incorrect.")
        return

    
    
    if withdrawal_amount <= 0:
        print("Error: You must enter a valid positive amount to withdraw.")
        return

    
    
    if withdrawal_amount > current_balance:
        print("Access Denied: There is not enough money in the account for this request.")
        return

    
    
    new_balance = current_balance - withdrawal_amount
    master_ledger[person_name]["money_in_cell"] = round(new_balance, 2)

    print(f"Success! {person_name} has withdrawn ${withdrawal_amount:.2f}.")
    print(f"The updated ledger now shows a balance of: ${new_balance:.2f}.")





print("--- Transaction 1 ---")
process_cash_request("Alice Smith", "1234", 50.00)


print("\n--- Transaction 2 ---")
process_cash_request("Bob Jones", "0000", 20.00)


print("\n--- Transaction 3 ---")
process_cash_request("Charlie Brown", "9012", 5000.00)


print("\n--- Transaction 4 ---")
process_cash_request("Unknown User", "1111", 10.00)