
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

    def calculate(self, operation, num1, num2):
        
        try:
            result = {
                '+': self.add(num1, num2),
                '-': self.subtract(num1, num2),
                '*': self.multiply(num1, num2),
                '/': self.divide(num1, num2)
            }[operation]
            return f"{num1} {operation} {num2} = {result}"
        except ValueError as e:
            return str(e)

    def print_history(self):
        
        for i, entry in enumerate(self.history, start=1):
            print(f"Entry {i}: {entry}")


def main():
    calc = Calculator()
    
    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")
        
        choice = input("Enter your choice (1/2/3/4/5): ")
        
        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            operation = choice
            print(calc.calculate(operation, num1, num2))
            
            
            calc.history.append(f"{num1} {operation} {num2}")
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please choose a valid operation.")

    print("\nCalculator History:")
    calc.print_history()


if __name__ == "__main__":
    main()
