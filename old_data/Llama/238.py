
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
        else:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")
            return result

    def calculate(self):
        print("\nCalculator History:")
        for entry in reversed(self.history):
            print(entry)
            print("-------------------")

def main():
    calculator = Calculator()
    
    while True:
        print("Operations Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")
        
        choice = input("\nChoose an operation (enter 1-5): ")
        
        if choice == '5':
            break
        
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        operations = {
            '1': calculator.add,
            '2': calculator.subtract,
            '3': calculator.multiply,
            '4': calculator.divide
        }
        
        try:
            result = operations[choice](num1, num2)
            print(f"\nResult: {result}")
        except ValueError as e:
            print(e)

if __name__ == "__main__":
    main()
