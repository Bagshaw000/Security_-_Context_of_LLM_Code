
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
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
        return result

    def calculate(self):
        
        while True:
            try:
                operation = input("Enter an operator (+, -, *, /): ")
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if operation == '+':
                    result = self.add(num1, num2)
                elif operation == '-':
                    result = self.subtract(num1, num2)
                elif operation == '*':
                    result = self.multiply(num1, num2)
                elif operation == '/':
                    result = self.divide(num1, num2)

                print("\nDo you want to perform another calculation? (yes/no)")
                response = input().lower()
                if response != 'yes':
                    break
            except ValueError as e:
                print(e)
                continue

    def display_history(self):
        
        print("Calculator History:")
        for i, item in enumerate(self.history, start=1):
            print(f"{i}. {item}")


def main():
    calculator = Calculator()

    while True:
        print("\n1. Perform a calculation")
        print("2. Display calculator history")
        print("3. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            calculator.calculate()
        elif choice == '2':
            calculator.display_history()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
