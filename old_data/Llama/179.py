
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

    def calculate(self):
        
        try:
            num1 = float(input("Enter first number: "))
            operator = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number: "))

            if operator == '+':
                result = self.add(num1, num2)
            elif operator == '-':
                result = self.subtract(num1, num2)
            elif operator == '*':
                result = self.multiply(num1, num2)
            elif operator == '/':
                result = self.divide(num1, num2)
            else:
                raise ValueError("Invalid operator")

            print(f"Result: {result}")
            self.history.append((num1, operator, num2, result))
        except ValueError as e:
            print(e)

    def display_history(self):
        
        if not self.history:
            print("No calculations performed yet.")
        else:
            for i, (num1, operator, num2, result) in enumerate(self.history):
                print(f"Calculation {i+1}: {num1} {operator} {num2} = {result}")


def main():
    calculator = Calculator()
    while True:
        print("Calculator Application")
        print("1. Perform calculation")
        print("2. Display calculation history")
        print("3. Quit")

        choice = input("Choose an option: ")

        if choice == '1':
            calculator.calculate()
        elif choice == '2':
            calculator.display_history()
        elif choice == '3':
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
