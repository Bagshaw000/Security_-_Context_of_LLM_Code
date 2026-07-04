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

    choice = input("Choose operation (+, -, *, /): ")

    if choice not in operations:
        print("Invalid choice.")
        return

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    result = operations[choice](num1, num2)

    print(f"{num1} {choice} {num2} = {result}")

if __name__ == "__main__":
    calculator()