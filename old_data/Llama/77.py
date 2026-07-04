
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

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            self.history.append(f"{expression} = {result}")
            return result
        except Exception as e:
            return str(e)

def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate Expression")
        print("6. View History")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            expression = input("Enter mathematical expression: ")
            try:
                result = calculator.calculate(expression)
                print(result)
            except Exception as e:
                print(e)
        elif choice == "6":
            if not calculator.history:
                print("No history available")
            else:
                print("\nCalculation History:")
                for entry in calculator.history:
                    print(entry)
        elif choice == "7":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
