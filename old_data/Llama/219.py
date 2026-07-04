
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        self.history.append((f"addition of {num1} and {num2}", result))

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        self.history.append((f"subtraction of {num1} and {num2}", result))

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append((f"multiplication of {num1} and {num2}", result))

    def divide(self, num1, num2):
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
            self.history.append((f"division of {num1} and {num2}", result))

    def display_history(self):
        if self.history:
            print("Calculation History:")
            for i, (expression, result) in enumerate(self.history, start=1):
                print(f"{i}. Expression: {expression}, Result: {result}")
        else:
            print("No calculation history.")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calculator.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calculator.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calculator.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))
            calculator.divide(num1, num2)
        elif choice == "5":
            calculator.display_history()
        elif choice == "6":
            print("Exiting the calculator.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
