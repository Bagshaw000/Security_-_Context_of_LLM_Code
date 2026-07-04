


print("Welcome to your Python Calculator, Harold!")
print("This works similarly to a formula in Excel.")



number1 = float(input("Enter your first number: "))


print("Choose an operation: + (add), - (subtract), * (multiply), / (divide)")
operation = input("Type the symbol and press Enter: ")


number2 = float(input("Enter your second number: "))


if operation == "+":
    result = number1 + number2
    print("The answer is:", result)

elif operation == "-":
    result = number1 - number2
    print("The answer is:", result)

elif operation == "*":
    result = number1 * number2
    print("The answer is:", result)

elif operation == "/":
    
    if number2 == 0:
        print("Error: You cannot divide by zero.")
    else:
        result = number1 / number2
        print("The answer is:", result)

else:
    print("The symbol you typed was not recognized. Please try again.")


input("Press Enter to exit.")