
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        return num1 + num2

    def subtract(self, num1, num2):
        
        return num1 - num2

    def multiply(self, num1, num2):
        
        return num1 * num2

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            self.history.append(f"Result: {result}")
            return result
        except Exception as e:
            self.history.append(f"Error: {str(e)}")
            return None

    def print_history(self):
        
        for i, entry in enumerate(self.history, start=1):
            print(f"{i}. {entry}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate a custom expression")
        print("6. Print history")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            try:
                num1 = float(input("Enter the dividend: "))
                num2 = float(input("Enter the divisor: "))
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            expression = input("Enter a mathematical expression: ")
            result = calculator.calculate(expression)
            if result is not None:
                print(f"Result: {result}")
        elif choice == "6":
            calculator.print_history()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
