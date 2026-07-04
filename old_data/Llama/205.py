
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

    def print_history(self):
        
        for i, entry in enumerate(self.history):
            print(f"{i+1}. {entry}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Print History")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "6":
            break
        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please try again.")
            continue

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if choice == "1":
            result = calculator.add(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif choice == "2":
            result = calculator.subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif choice == "3":
            result = calculator.multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif choice == "4":
            try:
                result = calculator.divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)

        calculator.print_history()


if __name__ == "__main__":
    main()
