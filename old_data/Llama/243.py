

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

    def calculate(self, operator, num1, num2):
        
        if operator == "+":
            return self.add(num1, num2)
        elif operator == "-":
            return self.subtract(num1, num2)
        elif operator == "*":
            return self.multiply(num1, num2)
        elif operator == "/":
            return self.divide(num1, num2)
        else:
            raise ValueError("Invalid operator")

    def display_history(self):
        
        print("\nCalculation History:")
        for i, entry in enumerate(self.history, start=1):
            print(f"{i}. {entry}")


def main():
    calculator = Calculator()
    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            operator = input("Enter operator (+, -, *, /): ")
            result = calculator.calculate(operator, num1, num2)

            print(f"Result: {result}")

            again = input("\nDo you want to calculate again? (y/n): ")
            if again.lower() != "y":
                break

        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
