import operator

def calculator():
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    print("Simple Calculator")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Choose an operation: ")

    if choice not in operations:
        return "Invalid choice"

    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    result = operations[choice](num1, num2)

    print(f"{num1} {choice} {num2} = {result}")

calculator()