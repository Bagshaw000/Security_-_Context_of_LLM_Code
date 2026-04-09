


print("--- Simple Calculator ---")
print("Instructions: Enter your numbers and the operation you want to perform.")
print("Type 'quit' to exit the program.")

while True:
    
    user_input1 = input("\nEnter the first number: ")
    if user_input1.lower() == 'quit':
        break
    
    
    operation = input("Enter the math symbol (+, -, *, /): ")
    
    
    user_input2 = input("Enter the second number: ")
    if user_input2.lower() == 'quit':
        break

    try:
        
        num1 = float(user_input1)
        num2 = float(user_input2)

        
        if operation == "+":
            result = num1 + num2
            print("The sum is:", result)
        elif operation == "-":
            result = num1 - num2
            print("The difference is:", result)
        elif operation == "*":
            result = num1 * num2
            print("The product is:", result)
        elif operation == "/":
            
            if num2 == 0:
                print("Error: You cannot divide by zero.")
            else:
                result = num1 / num2
                print("The result is:", result)
        else:
            print("Error: Please use a valid math symbol (+, -, *, /).")

    except ValueError:
        
        print("Error: Please enter valid numbers. Use digits only (e.g., 5 or 10.5).")

print("Calculator has been closed.")