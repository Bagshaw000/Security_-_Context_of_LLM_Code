
class Calculator:
    def __init__(self):
        pass

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


def main():
    calculator = Calculator()
    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        num1 = float(input("Enter the first number: "))
        operator = input("Enter the operator (+, -, *, /): ")
        num2 = float(input("Enter the second number: "))

        if operator == "+":
            print(f"{num1} + {num2} = {calculator.add(num1, num2)}")
        elif operator == "-":
            print(f"{num1} - {num2} = {calculator.subtract(num1, num2)}")
        elif operator == "*":
            print(f"{num1} * {num2} = {calculator.multiply(num1, num2)}")
        elif operator == "/":
            try:
                print(f"{num1} / {num2} = {calculator.divide(num1, num2)}")
            except ValueError as e:
                print(e)
        else:
            print("Invalid operator. Please try again.")

if __name__ == "__main__":
    main()
