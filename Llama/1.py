
class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b


class CalculatorApp:
    def __init__(self):
        self.calculator = Calculator()

    def run(self):
        while True:
            print("\n1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Exit")

            choice = input("Choose an operation (1/2/3/4/5): ")

            if choice in ['1', '2', '3', '4']:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    print(f"{num1} + {num2} = {self.calculator.add(num1, num2)}")
                elif choice == '2':
                    print(f"{num1} - {num2} = {self.calculator.subtract(num1, num2)}")
                elif choice == '3':
                    print(f"{num1} * {num2} = {self.calculator.multiply(num1, num2)}")
                elif choice == '4':
                    try:
                        print(f"{num1} / {num2} = {self.calculator.divide(num1, num2)}")
                    except ValueError as e:
                        print(e)
            elif choice == '5':
                break
            else:
                print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    app = CalculatorApp()
    app.run()
