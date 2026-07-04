import operator

def calculator():
    
    operators = {
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

    choice = input("Enter choice(1/2/3/4): ")

    num1 = float(input("Enter first number: "))
    num2 = float(input("Enter second number: "))

    if choice in operators:
        result = operators[choice](num1, num2)
        print(f"Result is {result}")
    else:
        print("Invalid input")

if __name__ == "__main__":
    calculator()