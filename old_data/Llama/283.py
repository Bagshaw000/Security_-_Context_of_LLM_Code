
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
        self.history.append((f"Subtraction: {num1} - {num2}", result))
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append((f"Multiplication: {num1} * {num2}", result))
        return result

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
            self.history.append((f"Division: {num1} / {num2}", result))
            return result
        else:
            print("Error! Division by zero is not allowed.")
            return None

    def display_history(self):
        
        if len(self.history) > 0:
            print("\nCalculator History:")
            for i, (op, result) in enumerate(self.history, start=1):
                print(f"{i}. {op} = {result}")
        else:
            print("\nNo operations performed yet.")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Choose an operation (1-6): ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.add(num1, num2)
        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.subtract(num1, num2)
        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.multiply(num1, num2)
        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))
            result = calculator.divide(num1, num2)
        elif choice == "5":
            calculator.display_history()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()
