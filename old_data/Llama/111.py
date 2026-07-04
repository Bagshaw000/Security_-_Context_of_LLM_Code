
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
        self.history.append(f"Multiplied {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, Result: {result}")
        return result

    def calculate(self):
        
        return self.history


def main():
    calc = Calculator()

    while True:
        print("Calculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")
        print("6. Exit")

        choice = input("Choose an operation (1-6): ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.add(num1, num2)
            print(f"Result: {result}")

        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.subtract(num1, num2)
            print(f"Result: {result}")

        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.multiply(num1, num2)
            print(f"Result: {result}")

        elif choice == "4":
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                result = calc.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))

        elif choice == "5":
            history = calc.calculate()
            for entry in history:
                print(entry)

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
