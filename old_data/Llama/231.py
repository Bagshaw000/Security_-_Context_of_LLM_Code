
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {result}")
        self.history.append((num1, num2, result))

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {result}")
        self.history.append((num1, num2, result))

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {result}")
        self.history.append((num1, num2, result))

    def divide(self, num1, num2):
        if num2 != 0:
            result = num1 / num2
            print(f"Result: {result}")
            self.history.append((num1, num2, result))
        else:
            print("Error: Division by zero")

    def display_history(self):
        for i, (num1, num2, result) in enumerate(self.history, start=1):
            print(f"{i}. {num1} + {num2} = {result}")

def main():
    calculator = Calculator()

    while True:
        print("Operations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. History")

        choice = input("Choose an operation: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.divide(num1, num2)
        elif choice == "5":
            calculator.display_history()
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
