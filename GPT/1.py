class Calculator:
    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            return "Error! Division by zero."
        return a / b

def main():
    calc = Calculator()
    while True:
        operation = input("Enter operation (+, -, *, /) or 'q' to quit: ")
        if operation == 'q':
            break
        if operation in ('+', '-', '*', '/'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                continue

            if operation == '+':
                print("Result:", calc.add(num1, num2))
            elif operation == '-':
                print("Result:", calc.subtract(num1, num2))
            elif operation == '*':
                print("Result:", calc.multiply(num1, num2))
            elif operation == '/':
                print("Result:", calc.divide(num1, num2))
        else:
            print("Invalid operation. Please try again.")

if __name__ == "__main__":
    main()