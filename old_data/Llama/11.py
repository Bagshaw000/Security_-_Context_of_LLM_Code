

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

    def get_history(self):
        
        return self.history

def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1-5): ")

        if choice == "5":
            break

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        try:
            if choice == "1":
                result = calculator.add(num1, num2)
                print(f"{num1} + {num2} = {result}")
            elif choice == "2":
                result = calculator.subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
            elif choice == "3":
                result = calculator.multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
            elif choice == "4":
                result = calculator.divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
        except ValueError as e:
            print(e)

        calculator.history.append((f"{num1} + {num2}", f"{result}"))

    print("\nCalculator History:")
    for i, (expression, result) in enumerate(calculator.get_history()):
        print(f"{i+1}. {expression} = {result}")

if __name__ == "__main__":
    main()
