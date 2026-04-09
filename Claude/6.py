print("Welcome to the Calculator!")
num1 = float(input("Enter the first number: "))
operator = input("Enter the operator (+, -, *, /): ")
num2 = float(input("Enter the second number: "))

if operator == "+":
    result = num1 + num2
    print("The result is:", result)
elif operator == "-":
    result = num1 - num2
    print("The result is:", result)
elif operator == "*":
    result = num1 * num2
    print("The result is:", result)
elif operator == "/":
    if num2 == 0:
        print("Error: Cannot divide by zero.")
    else:
        result = num1 / num2
        print("The result is:", result)
else:
    print("Error: Invalid operator.")