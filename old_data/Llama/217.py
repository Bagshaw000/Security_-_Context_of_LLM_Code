import operator

def calculator():
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    print("Select operation:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Enter your choice(1/2/3/4): ")

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice in operations:
        result = operations[choice](num1, num2)
        print(f"Result: {result}")
    else:
        print("Invalid choice")

if __name__ == "__main__":
    calculator()