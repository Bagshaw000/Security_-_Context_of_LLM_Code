
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        self.history.append((num1, num2, result))
        return result

    def subtract(self, num1, num2):
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        self.history.append((num1, num2, result))
        return result

    def multiply(self, num1, num2):
        result = num1 * num2
        print(f"Result: {num1} × {num2} = {result}")
        self.history.append((num1, num2, result))
        return result

    def divide(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        print(f"Result: {num1} ÷ {num2} = {result}")
        self.history.append((num1, num2, result))
        return result

    def display_history(self):
        for i, (num1, num2, result) in enumerate(self.history):
            print(f"{i+1}. {num1} {('+' if num2 > num1 else '-')} {num2} = {result}")


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
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                calculator.divide(num1, num2)
            except ValueError as e:
                print(e)
        elif choice == "5":
            calculator.display_history()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
