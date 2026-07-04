
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
        
        if num2 != 0:
            result = num1 / num2
            self.history.append(f"{num1} / {num2} = {result}")
            return result
        else:
            raise ValueError("Cannot divide by zero")

    def get_history(self):
        
        return self.history


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")
        print("6. Quit")

        choice = input("Choose an operation (1-6): ")

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
                print(str(e))
        elif choice == "5":
            print("\nCalculator History:")
            for i, item in enumerate(calculator.get_history(), start=1):
                print(f"{i}. {item}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main()
