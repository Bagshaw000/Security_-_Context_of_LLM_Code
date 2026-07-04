
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        self.history.append(f"Added {num1} and {num2}, Result: {result}")

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append(f"Multiplied {num1} and {num2}, Result: {result}")

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error! Division by zero.")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")

    def display_history(self):
        
        print("Calculator History:")
        for i, entry in enumerate(self.history, start=1):
            print(f"{i}. {entry}")


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calc.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calc.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            calc.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))
            calc.divide(num1, num2)
        elif choice == "5":
            calc.display_history()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
