
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
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        return result

    def get_history(self):
        
        return self.history


def main():
    calculator = Calculator()
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if choice == "1":
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
            calculator.history.append((f"{num1} + {num2}", result))
        elif choice == "2":
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
            calculator.history.append((f"{num1} - {num2}", result))
        elif choice == "3":
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
            calculator.history.append((f"{num1} * {num2}", result))
        elif choice == "4":
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
                calculator.history.append((f"{num1} / {num2}", result))
            except ValueError as e:
                print(str(e))

    print("\nCalculation History:")
    for i, (expr, result) in enumerate(calculator.get_history(), 1):
        print(f"{i}. {expr}: {result}")


if __name__ == "__main__":
    main()
