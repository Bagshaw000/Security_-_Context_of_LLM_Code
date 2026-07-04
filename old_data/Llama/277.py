import operator

def calculator():
    print("Calculator Application")
    print("--------------------")

    while True:
        print("\n1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1/2/3/4/5): ")

        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                print(f"{num1} + {num2} = {operator.add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {operator.sub(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {operator.mul(num1, num2)}")
            elif choice == '4':
                if num2 != 0:
                    print(f"{num1} / {num2} = {operator.truediv(num1, num2)}")
                else:
                    print("Error! Division by zero is not allowed.")
        elif choice == '5':
            print("Thank you for using the calculator application.")
            break
        else:
            print("Invalid input. Please enter a number between 1 and 5.")

calculator()