import operator

def calculator():
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    print("Calculator Application")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Enter your choice (1-4): ")

    if choice in operations:
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        result = operations[choice](num1, num2)

        print(f"{num1} {choice} {num2} = {result}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    calculator()