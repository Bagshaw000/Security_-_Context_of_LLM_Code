
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

    def display_history(self):
        
        print("\nCalculator History:")
        for entry in reversed(self.history):
            print(entry)


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

        if choice == "6":
            break

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == "1":
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))
        elif choice == "5":
            calculator.display_history()
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
