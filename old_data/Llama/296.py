
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
            raise ValueError("Cannot divide by zero.")
        return num1 / num2

    def calculate(self, operation, num1, num2):
        
        operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide
        }
        if operation in operations:
            return operations[operation](num1, num2)
        else:
            raise ValueError("Invalid operation.")

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
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            operation = input("Enter operation (+, -, *, /): ")
            try:
                result = calculator.calculate(operation, num1, num2)
                print(f"{num1} {operation} {num2} = {result}")
                calculator.history.append(f"{num1} {operation} {num2} = {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            break
        else:
            print("Invalid choice. Please try again.")

    print("\nCalculation History:")
    for i, history in enumerate(calculator.get_history(), start=1):
        print(f"{i}. {history}")

if __name__ == "__main__":
    main()
