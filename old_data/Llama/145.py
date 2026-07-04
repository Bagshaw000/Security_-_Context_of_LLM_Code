import operator

def calculator():
    print("Select an operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Enter the number of your chosen operation: ")

    if choice in ['1', '2', '3', '4']:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        operations = {
            '1': operator.add,
            '2': operator.sub,
            '3': operator.mul,
            '4': operator.truediv
        }

        func = operations[choice]
        result = func(num1, num2)

        print(f"{num1} {choice.upper()} {num2} = {result}")

    else:
        print("Invalid choice")

if __name__ == "__main__":
    calculator()