



while True:
    print("\n--- Simple Calculator ---")
    
    
    entry1 = input("Enter the first number (or type 'quit'): ")
    if entry1.lower() == 'quit':
        break
        
    
    operation = input("Enter the operation (+, -, *, /): ")
    
    
    entry2 = input("Enter the second number: ")
    if entry2.lower() == 'quit':
        break

    try:
        
        num1 = float(entry1)
        num2 = float(entry2)

        
        if operation == '+':
            result = num1 + num2
            print("The answer is:", result)
        elif operation == '-':
            result = num1 - num2
            print("The answer is:", result)
        elif operation == '*':
            result = num1 * num2
            print("The answer is:", result)
        elif operation == '/':
            
            if num2 == 0:
                print("Error: You cannot divide by zero.")
            else:
                result = num1 / num2
                print("The answer is:", result)
        else:
            print("Error: Please use a valid symbol (+, -, *, or /).")
            
    except ValueError:
        
        print("Error: Please ensure you are entering numbers.")

print("The program has closed. Goodbye, Harold!")