
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        self.history.append((f"{num1} + {num2}", result))
        return result

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        self.history.append((f"{num1} - {num2}", result))
        return result

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
        self.history.append((f"{num1} * {num2}", result))
        return result

    def divide(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        print(f"Result: {num1} / {num2} = {result}")
        self.history.append((f"{num1} / {num2}", result))
        return result

    def calculate(self, operation, *args):
        if operation == '+':
            return self.add(*args)
        elif operation == '-':
            return self.subtract(*args)
        elif operation == '*':
            return self.multiply(*args)
        elif operation == '/':
            return self.divide(*args)
        else:
            raise ValueError("Invalid operation")

def main():
    calculator = Calculator()
    while True:
        print("\n1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")
        choice = input("Enter your choice: ")
        if choice == '5':
            break
        elif choice not in ['1', '2', '3', '4']:
            print("Invalid choice")
            continue

        operation = input("Enter the operation (+, -, *, /): ")
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        try:
            result = calculator.calculate(operation, num1, num2)
        except ValueError as e:
            print(str(e))
            continue

if __name__ == "__main__":
    main()
