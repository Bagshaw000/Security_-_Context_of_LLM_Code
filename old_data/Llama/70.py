import operator

def calculator():
    operations = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }

    print("Select operation:")
    print("+  Addition")
    print("-  Subtraction")
    print("*  Multiplication")
    print("/  Division")

    user_input = input("Enter the operation (+, -, *, /): ")
    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if user_input in operations:
        result = operations[user_input](num1, num2)
        print(f"{num1} {user_input} {num2} = {result}")
    else:
        print("Invalid operation")

calculator()