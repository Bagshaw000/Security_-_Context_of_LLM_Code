
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

    def calculate(self, num1, operator, num2):
        
        if operator == "+":
            return self.add(num1, num2)
        elif operator == "-":
            return self.subtract(num1, num2)
        elif operator == "*":
            return self.multiply(num1, num2)
        elif operator == "/":
            return self.divide(num1, num2)
        else:
            raise ValueError("Invalid operator")

def main():
    calculator = Calculator()

    while True:
        print("\nMenu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate with operator (+, -, *, /)")
        print("6. History")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.divide(num1, num2)
            except ValueError as e:
                print(e)
        elif choice == "5":
            num1 = float(input("Enter first number: "))
            operator = input("Enter operator (+, -, *, /): ")
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.calculate(num1, operator, num2)
            except ValueError as e:
                print(e)
        elif choice == "6":
            if calculator.history:
                print("\nHistory:")
                for i, item in enumerate(calculator.history):
                    print(f"{i+1}. {item}")
            else:
                print("No calculations performed yet.")
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please try again.")

        if result is not None:
            calculator.history.append(str(result))

if __name__ == "__main__":
    main()
