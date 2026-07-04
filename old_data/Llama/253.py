
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, Result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, Result: {result}")
        return result

    def calculate(self, operation, num1, num2):
        
        if operation == "+":
            return self.add(num1, num2)
        elif operation == "-":
            return self.subtract(num1, num2)
        elif operation == "*":
            return self.multiply(num1, num2)
        elif operation == "/":
            return self.divide(num1, num2)
        else:
            raise ValueError("Invalid operation.")

    def print_history(self):
        
        for i, result in enumerate(self.history):
            print(f"{i+1}. {result}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1-5): ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("+", num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("-", num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("*", num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = calculator.calculate("/", num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")

        response = input("\nWould you like to view the calculation history? (y/n): ")
        if response.lower() == "y":
            calculator.print_history()

if __name__ == "__main__":
    main()
