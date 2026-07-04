
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
            return None
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")
            return result

    def history(self):
        for i, (operation, result) in enumerate(self.history, start=1):
            print(f"{i}. {operation}: {result}")


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
            result = calculator.divide(num1, num2)
            if result is not None:
                calculator.history().append((f"Division", f"{num1} / {num2} = {result}" ))
        elif choice == "5":
            calculator.history()
        elif choice == "6":
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
