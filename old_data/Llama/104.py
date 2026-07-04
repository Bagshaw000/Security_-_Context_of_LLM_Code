
import math

class Calculator:
    def __init__(self):
        self.history = []

    
    def add(self, num1, num2):
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, Result: {result}")
        return result

    
    def sub(self, num1, num2):
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")
        return result

    
    def mul(self, num1, num2):
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, Result: {result}")
        return result

    
    def div(self, num1, num2):
        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        else:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")
            return result

    
    def show_history(self):
        if not self.history:
            print("No calculations have been performed yet.")
        else:
            for i, calculation in enumerate(self.history, start=1):
                print(f"Calculation {i}: {calculation}")


def main():
    calculator = Calculator()

    while True:
        
        print("\nCalculator Menu:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Show History")
        print("6. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.sub(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.mul(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = calculator.div(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)
        elif choice == "5":
            calculator.show_history()
        elif choice == "6":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
