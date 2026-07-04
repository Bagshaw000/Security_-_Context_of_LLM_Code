
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {result}")
        self.history.append(f"{num1} + {num2} = {result}")

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {result}")
        self.history.append(f"{num1} - {num2} = {result}")

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {result}")
        self.history.append(f"{num1} * {num2} = {result}")

    def divide(self, num1, num2):
        if num2 != 0:
            result = num1 / num2
            print(f"Result: {result}")
            self.history.append(f"{num1} / {num2} = {result}")
        else:
            print("Error: Division by zero is not allowed")

    def display_history(self):
        for i, entry in enumerate(self.history):
            print(f"{i+1}. {entry}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Exit")

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
        elif choice == "6":
            print("Exiting application")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
