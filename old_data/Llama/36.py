
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result: {result}")
        return result

    def calculate(self, op, num1, num2):
        
        if op == "+":
            return self.add(num1, num2)
        elif op == "-":
            return self.subtract(num1, num2)
        elif op == "*":
            return self.multiply(num1, num2)
        elif op == "/":
            return self.divide(num1, num2)
        else:
            raise ValueError("Invalid operation")

    def display_history(self):
        
        for i, entry in enumerate(self.history):
            print(f"Entry {i+1}: {entry}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate (with operator)")
        print("6. Display History")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")

        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")

        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")

        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))

        elif choice == "5":
            op = input("Enter operator (+, -, *, /): ")
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.calculate(op, num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))

        elif choice == "6":
            calculator.display_history()

        elif choice == "7":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
