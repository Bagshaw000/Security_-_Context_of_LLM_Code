
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error: Division by zero is not allowed")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
        return result

    def history(self):
        
        for i, item in enumerate(self.history, start=1):
            print(f"Calculation {i}: {item}")


def main():
    calculator = Calculator()

    while True:
        print("Calculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")
        print("6. Quit")

        choice = input("Choose an operation (1-6): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == '1':
                result = calculator.add(num1, num2)
            elif choice == '2':
                result = calculator.subtract(num1, num2)
            elif choice == '3':
                result = calculator.multiply(num1, num2)
            else:
                result = calculator.divide(num1, num2)

        elif choice == '5':
            calculator.history()

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()
