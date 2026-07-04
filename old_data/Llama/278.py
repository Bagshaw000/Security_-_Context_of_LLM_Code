
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
        
        if num2 != 0:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")
            self.history.append((f"{num1} / {num2}", result))
            return result
        else:
            print("Error: Division by zero is not allowed")
            return None

    def display_history(self):
        
        print("\nCalculator History:")
        for i, (expression, result) in enumerate(self.history, start=1):
            print(f"{i}. {expression} = {result}")


def main():
    calculator = Calculator()

    while True:
        print("\n\nCalculator Menu")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        if choice == "6":
            break
        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                result = calculator.add(num1, num2)
            elif choice == "2":
                result = calculator.subtract(num1, num2)
            elif choice == "3":
                result = calculator.multiply(num1, num2)
            elif choice == "4":
                result = calculator.divide(num1, num2)

        elif choice == "5":
            calculator.display_history()

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
