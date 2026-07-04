
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
        try:
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
        except ValueError as e:
            print(e)

    def display_history(self):
        if not self.history:
            print("No calculations history")
        else:
            for i, entry in enumerate(self.history, start=1):
                print(f"Calculation {i}: {entry}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nCalculator Menu:")
        print("1. Perform calculation")
        print("2. Display calculations history")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            operation = input("Enter operation (+, -, *, /): ")
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            try:
                result = calculator.calculate(operation, num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)

        elif choice == "2":
            calculator.display_history()

        elif choice == "3":
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
