
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
            raise ValueError("Cannot divide by zero!")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, Result: {result}")
        return result

    def calculate(self, operation, *args):
        
        if operation == "add":
            return self.add(*args)
        elif operation == "subtract":
            return self.subtract(*args)
        elif operation == "multiply":
            return self.multiply(*args)
        elif operation == "divide":
            return self.divide(*args)
        else:
            raise ValueError("Invalid operation!")

    def display_history(self):
        
        print("\nCalculation History:")
        for entry in reversed(self.history):
            print(entry)


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate History")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("add", num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("subtract", num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.calculate("multiply", num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            try:
                num1 = float(input("Enter dividend: "))
                num2 = float(input("Enter divisor: "))
                result = calculator.calculate("divide", num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            calculator.display_history()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
