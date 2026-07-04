
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
            raise ValueError("Cannot divide by zero")
        return num1 / num2

    def calculate(self, num1, operation, num2):
        
        result = None
        if operation == '+':
            result = self.add(num1, num2)
        elif operation == '-':
            result = self.subtract(num1, num2)
        elif operation == '*':
            result = self.multiply(num1, num2)
        elif operation == '/':
            result = self.divide(num1, num2)
        else:
            raise ValueError("Invalid operation")
        
        self.history.append(f"{num1} {operation} {num2} = {result}")
        return result

    def print_history(self):
        
        for i, calc in enumerate(self.history, start=1):
            print(f"Calculation {i}: {calc}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate and Print History")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate(num1, '+', num2)
            print(f"Result: {result}")
        elif choice == '2':
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate(num1, '-', num2)
            print(f"Result: {result}")
        elif choice == '3':
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate(num1, '*', num2)
            print(f"Result: {result}")
        elif choice == '4':
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = calculator.calculate(num1, '/', num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == '5':
            calculator.print_history()
        elif choice == '6':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
