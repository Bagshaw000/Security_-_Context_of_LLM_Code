
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
            print("Error: Division by zero is not allowed.")

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
            print("Error: Invalid operation.")

    def display_history(self):
        
        for i, result in enumerate(self.history, start=1):
            print(f"{i}. {result}")


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

        if choice == "6":
            break

        elif choice in ["1", "2", "3"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            operation = input(f"Choose an operation ({'add', 'subtract', 'multiply'}): ")
            if operation == "add":
                result = calculator.add(num1, num2)
            elif operation == "subtract":
                result = calculator.subtract(num1, num2)
            else:
                result = calculator.multiply(num1, num2)

            print(f"{num1} {operation} {num2} = {result}")

        elif choice == "5":
            calculator.display_history()

        else:
            print("Error: Invalid choice.")


if __name__ == "__main__":
    main()
