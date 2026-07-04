
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
            raise ValueError("Cannot divide by zero!")
        return num1 / num2

    def calculate(self, operation, num1, num2):
        
        operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide
        }
        try:
            if operation in operations:
                return operations[operation](num1, num2)
            else:
                raise ValueError("Invalid operation!")
        except Exception as e:
            print(f"Error: {e}")
            return None

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
        print("5. History")
        print("6. Exit")
        
        choice = input("Enter your choice: ")
        
        if choice == "6":
            break
        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice! Please try again.")
            continue
        
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        operation = input("Enter the operation (+, -, *, /): ")
        
        result = calculator.calculate(operation, num1, num2)
        
        if result is not None:
            print(f"{num1} {operation} {num2} = {result}")
            calculator.history.append((f"{num1} {operation} {num2}", result))


if __name__ == "__main__":
    main()
