import operator

def calculator():
    print("Calculator Application")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Enter your choice (1, 2, 3, 4): ")

    if choice in ('1', '2', '3', '4'):
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == '1':
            result = operator.add(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif choice == '2':
            result = operator.sub(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif choice == '3':
            result = operator.mul(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif choice == '4':
            if num2 != 0:
                result = operator.truediv(num1, num2)
                print(f"{num1} / {num2} = {result}")
            else:
                print("Error! Division by zero is not allowed.")
    else:
        print("Invalid input. Please choose a valid option.")

calculator()