import operator

def calculator():
    print("Welcome to the Calculator Application")
    while True:
        try:
            num1 = float(input("Enter first number: "))
            operation = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))

            if operation == '+':
                result = num1 + num2
            elif operation == '-':
                result = num1 - num2
            elif operation == '*':
                result = num1 * num2
            elif operation == '/':
                if num2 != 0:
                    result = num1 / num2
                else:
                    print("Error! Division by zero is not allowed.")
            else:
                print("Invalid operation. Please try again.")

            print(f"{num1} {operation} {num2} = {result}")

        except ValueError:
            print("Invalid input. Please enter a valid number.")

        cont = input("Do you want to continue? (yes/no): ")
        if cont.lower() != 'yes':
            break

calculator()