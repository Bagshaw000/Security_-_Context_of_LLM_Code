
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"{num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"{num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"{num1} / {num2} = {result}")
        return result

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            print(f"Error: {str(e)}")

def main():
    calculator = Calculator()
    while True:
        print("\n1. Basic Arithmetic Operations")
        print("2. Evaluate a Mathematical Expression")
        print("3. View History")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
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
                    print(str(e))
        elif choice == "2":
            expression = input("Enter a mathematical expression: ")
            try:
                result = calculator.calculate(expression)
                print(f"Result: {result}")
            except Exception as e:
                print(str(e))
        elif choice == "3":
            if not calculator.history:
                print("No calculation history")
            else:
                for i, entry in enumerate(calculator.history):
                    print(f"{i+1}. {entry}")
        elif choice == "4":
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
