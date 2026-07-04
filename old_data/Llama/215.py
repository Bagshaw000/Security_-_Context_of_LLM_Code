import operator

def calculator():
    while True:
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Choose an operation: ")

        if choice == "5":
            break

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        operators = {
            1: operator.add,
            2: operator.sub,
            3: operator.mul,
            4: operator.truediv
        }

        if choice in operators:
            result = operators[choice](num1, num2)

            print(f"{num1} {choice.upper()} {num2} = {result}")
        else:
            print("Invalid choice")

if __name__ == "__main__":
    calculator()