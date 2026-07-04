import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            logging.error("Division by zero attempted.")
            raise ValueError("Cannot divide by zero.")
        return a / b

class InputValidator:
    @staticmethod
    def validate_number(value):
        try:
            number = float(value)
            return number
        except ValueError:
            logging.error(f"Invalid input: {value} is not a number.")
            raise ValueError(f"Invalid input: {value} is not a number.")

class CalculatorService:
    def __init__(self):
        self.calculator = Calculator()

    def perform_operation(self, operation, a, b):
        a = InputValidator.validate_number(a)
        b = InputValidator.validate_number(b)

        if operation == 'add':
            return self.calculator.add(a, b)
        elif operation == 'subtract':
            return self.calculator.subtract(a, b)
        elif operation == 'multiply':
            return self.calculator.multiply(a, b)
        elif operation == 'divide':
            return self.calculator.divide(a, b)
        else:
            logging.error(f"Invalid operation: {operation}")
            raise ValueError(f"Invalid operation: {operation}")

class CalculatorApp:
    def __init__(self):
        self.service = CalculatorService()

    def run(self):
        while True:
            try:
                operation = input("Enter operation (add, subtract, multiply, divide) or 'exit' to quit: ")
                if operation.lower() == 'exit':
                    break
                a = input("Enter first number: ")
                b = input("Enter second number: ")
                result = self.service.perform_operation(operation, a, b)
                print(f"Result: {result}")
            except Exception as e:
                logging.error(f"An error occurred: {e}")
                print(f"Error: {e}")

if __name__ == "__main__":
    app = CalculatorApp()
    app.run()