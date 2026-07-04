
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        return result

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            return result
        else:
            return "Error: Division by zero is not allowed"

    def calculate(self, operation, num1, num2=None):
        
        if operation == "+":
            return self.add(num1, num2)
        elif operation == "-":
            return self.subtract(num1, num2)
        elif operation == "*":
            return self.multiply(num1, num2)
        elif operation == "/":
            return self.divide(num1, num2)

    def print_history(self):
        
        for i, result in enumerate(self.history):
            print(f"Operation {i+1}: {result}")


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1-5): ")

        if choice == "5":
            break

        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please choose a valid option.")
            continue

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number (if applicable): "))

        if choice == "4":
            result = calc.divide(num1, num2)
        else:
            result = calc.calculate(choice, num1, num2)

        print(f"Result: {result}")

        
        calc.history.append(result)

    calc.print_history()


if __name__ == "__main__":
    main()
