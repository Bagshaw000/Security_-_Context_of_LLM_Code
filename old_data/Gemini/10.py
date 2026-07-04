


print("Welcome to your Python Calculator.")



first_number = float(input("Please type your first number: "))


operation = input("Type the symbol for the math you want to do (+, -, *, /): ")


second_number = float(input("Please type your second number: "))




if operation == "+":
    result = first_number + second_number
    print("The answer is:", result)

elif operation == "-":
    result = first_number - second_number
    print("The answer is:", result)

elif operation == "*":
    result = first_number * second_number
    print("The answer is:", result)

elif operation == "/":
    
    if second_number == 0:
        print("Error: You cannot divide by zero.")
    else:
        result = first_number / second_number
        print("The answer is:", result)

else:
    
    print("Sorry, that symbol was not recognized.")


input("Press the Enter key to exit.")