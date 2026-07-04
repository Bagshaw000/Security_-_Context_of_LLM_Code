
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        self.history.append(f"{num1} + {num2} = {result}")

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        self.history.append(f"{num1} - {num2} = {result}")

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append(f"{num1} * {num2} = {result}")

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
            self.history.append(f"{num1} / {num2} = {result}")
        else:
            print("Error: Division by zero is not allowed")

    def display_history(self):
        
        print("\nCalculator History:")
        for i, entry in enumerate(self.history, start=1):
            print(f"Entry {i}: {entry}")


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

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calc.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calc.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calc.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calc.divide(num1, num2)
        elif choice == "5":
            calc.display_history()
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose a valid option.")

if __name__ == "__main__":
    main()
