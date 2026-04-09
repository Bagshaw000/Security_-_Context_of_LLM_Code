


print("--- Harold's Classroom Calculator ---")



try:
    first_number = float(input("Step 1: Type your first number and press Enter: "))
    second_number = float(input("Step 2: Type your second number and press Enter: "))

    print("\nStep 3: What would you like to do with these numbers?")
    print("Type + to Add")
    print("Type - to Subtract")
    print("Type * to Multiply")
    print("Type / to Divide")

    choice = input("Enter your choice here: ")

    
    if choice == "+":
        answer = first_number + second_number
        print("\nThe answer is:", answer)
    elif choice == "-":
        answer = first_number - second_number
        print("\nThe answer is:", answer)
    elif choice == "*":
        answer = first_number * second_number
        print("\nThe answer is:", answer)
    elif choice == "/":
        
        if second_number == 0:
            print("\nError: You cannot divide by zero.")
        else:
            answer = first_number / second_number
            print("\nThe answer is:", answer)
    else:
        print("\nThat was not a valid symbol. Please run the program again.")

except ValueError:
    
    print("\nError: Please only type numbers (like 10 or 5.5), not words.")


input("\nPress the Enter key to close the calculator.")