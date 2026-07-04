
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

    def get_result(self, operation, num1, num2):
        
        try:
            operations = {
                '+': self.add,
                '-': self.subtract,
                '*': self.multiply,
                '/': self.divide
            }
            if operation not in operations:
                raise ValueError("Invalid operator")
            return operations[operation](num1, num2)
        except Exception as e:
            print(f"An error occurred: {str(e)}")

    def display_history(self):
        
        for i, result in enumerate(self.history, start=1):
            print(f"{i}. {result}")


def main():
    calculator = Calculator()
    
    while True:
        operation = input("Enter an operation (+, -, *, /), or 'q' to quit: ")
        
        if operation.lower() == 'q':
            break
        
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            result = calculator.get_result(operation, num1, num2)
            print(f"{num1} {operation} {num2} = {result}")
            calculator.history.append(result)
        except ValueError as e:
            print(e)


if __name__ == "__main__":
    main()
