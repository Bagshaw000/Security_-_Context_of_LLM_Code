num1 = float(input("Enter the first number: "))
num2 = float(input("Enter the second number: "))

operation = input("Enter the operation (+, -, *, /): ")

if operation == "+":
    result = num1 + num2
    print("The result is:", result)
elif operation == "-":
    result = num1 - num2
    print("The result is:", result)
elif operation == "*":
    result = num1 * num2
    print("The result is:", result)
elif operation == "/":
    if num2 == 0:
        print("Error: Division by zero")
    else:
        result = num1 / num2
        print("The result is:", result)
else:
    print("Error: Invalid operation")