





try:
    
    
    
    
    
    

    number_one = float(input("Please enter your first number: "))
    number_two = float(input("Please enter your second number: "))

    
    
    print("Select an operation: + (Add), - (Subtract), * (Multiply), / (Divide)")
    operation = input("Enter the symbol for the operation: ")

    
    
    

    if operation == '+':
        result = number_one + number_two
        print(f"The result of adding {number_one} and {number_two} is: {result}")

    elif operation == '-':
        result = number_one - number_two
        print(f"The result of subtracting {number_two} from {number_one} is: {result}")

    elif operation == '*':
        result = number_one * number_two
        print(f"The result of multiplying {number_one} by {number_two} is: {result}")

    elif operation == '/':
        
        
        
        
        if number_two == 0:
            print("Error: You cannot divide by zero. Please try again with a different divisor.")
        else:
            result = number_one / number_two
            print(f"The result of dividing {number_one} by {number_two} is: {result}")

    else:
        
        print("Error: The symbol you entered is not a recognized mathematical operator.")

except ValueError:
    
    
    
    
    print("Input Error: You must enter valid numeric digits. Please restart the program.")




