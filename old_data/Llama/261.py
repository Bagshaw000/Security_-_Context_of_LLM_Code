
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, Result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplicated {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, Result: {result}")
        return result

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            self.history.append(f"Evaluated '{expression}', Result: {result}")
            return result
        except Exception as e:
            print(f"Error: {str(e)}")

    def display_history(self):
        
        if not self.history:
            print("No calculations performed")
        else:
            for i, calculation in enumerate(self.history, start=1):
                print(f"{i}. {calculation}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate Expression")
        print("6. Display History")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(f"Error: {str(e)}")
        elif choice == "5":
            expression = input("Enter a mathematical expression: ")
            result = calculator.calculate(expression)
            if isinstance(result, str):
                print(result)
            else:
                print(f"Result: {result}")
        elif choice == "6":
            calculator.display_history()
        elif choice == "7":
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
