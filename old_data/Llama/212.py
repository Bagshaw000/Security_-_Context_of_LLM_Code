
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        self.history.append((f"{num1} + {num2}", result))

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        self.history.append((f"{num1} - {num2}", result))

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
        self.history.append((f"{num1} * {num2}", result))

    def divide(self, num1, num2):
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")
            self.history.append((f"{num1} / {num2}", result))

    def display_history(self):
        print("\nCalculation History:")
        for i, (operation, result) in enumerate(self.history, 1):
            print(f"{i}. Operation: {operation}, Result: {result}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Choose an operation (1-6): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                calculator.add(num1, num2)
            elif choice == "2":
                calculator.subtract(num1, num2)
            elif choice == "3":
                calculator.multiply(num1, num2)
            elif choice == "4":
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
