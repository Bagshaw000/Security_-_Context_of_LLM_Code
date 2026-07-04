
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        return f"{num1} + {num2} = {result}"
        
    def subtract(self, num1, num2):
        
        result = num1 - num2
        return f"{num1} - {num2} = {result}"

    def multiply(self, num1, num2):
        
        result = num1 * num2
        return f"{num1} * {num2} = {result}"

    def divide(self, num1, num2):
        
        if num2 == 0:
            return "Error: Division by zero is not allowed"
        result = num1 / num2
        return f"{num1} / {num2} = {result}"

    def calculate(self, num1, operator, num2):
        
        if operator == '+':
            return self.add(num1, num2)
        elif operator == '-':
            return self.subtract(num1, num2)
        elif operator == '*':
            return self.multiply(num1, num2)
        elif operator == '/':
            return self.divide(num1, num2)
        else:
            return "Invalid operator"

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
        
        if choice == '1':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.calculate(num1, '+', num2)
            print(result)
            calculator.history.append(f"{num1} + {num2} = {result}")
            
        elif choice == '2':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.calculate(num1, '-', num2)
            print(result)
            calculator.history.append(f"{num1} - {num2} = {result}")
            
        elif choice == '3':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.calculate(num1, '*', num2)
            print(result)
            calculator.history.append(f"{num1} * {num2} = {result}")
            
        elif choice == '4':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.calculate(num1, '/', num2)
            print(result)
            calculator.history.append(f"{num1} / {num2} = {result}")
            
        elif choice == '5':
            break
            
        else:
            print("Invalid choice. Please try again.")

def display_history():
    print("\nCalculator History:")
    for i, history in enumerate(calculator.history):
        print(f"Step {i+1}: {history}")

if __name__ == "__main__":
    main()
