

def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y


class Calculator:
    def __init__(self):
        pass

    
    def add(self, x, y):
        return add(x, y)

    
    def subtract(self, x, y):
        return subtract(x, y)

    
    def multiply(self, x, y):
        return multiply(x, y)

    
    def divide(self, x, y):
        return divide(x, y)


calculator = Calculator()


while True:
    print("\nCalculator Menu:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Quit")

    choice = input("Enter your choice (1-5): ")

    if choice == "1":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calculator.add(num1, num2)
        print(f"{num1} + {num2} = {result}")

    elif choice == "2":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calculator.subtract(num1, num2)
        print(f"{num1} - {num2} = {result}")

    elif choice == "3":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calculator.multiply(num1, num2)
        print(f"{num1} * {num2} = {result}")

    elif choice == "4":
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.divide(num1, num2)
            print(f"{num1} / {num2} = {result}")
        except ValueError as e:
            print(str(e))

    elif choice == "5":
        break

    else:
        print("Invalid choice. Please try again.")
