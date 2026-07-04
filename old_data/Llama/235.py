
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiply {num1} and {num2}, result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result: {result}")
        return result

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            return f"{expression} evaluates to {result}"
        except Exception as e:
            return str(e)

def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate Expression")
        print("6. View History")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calc.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calc.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calc.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calc.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))
        elif choice == "5":
            expression = input("Enter mathematical expression: ")
            result = calc.calculate(expression)
            print(result)
        elif choice == "6":
            print("\nCalculator History:")
            for entry in calc.history:
                print(entry)
        elif choice == "7":
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
