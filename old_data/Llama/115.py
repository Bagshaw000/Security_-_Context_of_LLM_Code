
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        return f"{num1} + {num2} = {result}"

    def subtract(self, num1, num2):
        result = num1 - num2
        return f"{num1} - {num2} = {result}"

    def multiply(self, num1, num2):
        result = num1 * num2
        return f"{num1} * {num2} = {result}"

    def divide(self, num1, num2):
        if num2 == 0:
            return "Error: Division by zero is not allowed"
        else:
            result = num1 / num2
            return f"{num1} / {num2} = {result}"

    def print_history(self):
        for i, operation in enumerate(self.history, start=1):
            print(f"Operation {i}: {operation}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Print History")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                print(calculator.add(num1, num2))
            elif choice == "2":
                print(calculator.subtract(num1, num2))
            elif choice == "3":
                print(calculator.multiply(num1, num2))
            elif choice == "4":
                print(calculator.divide(num1, num2))

        elif choice == "5":
            calculator.print_history()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
