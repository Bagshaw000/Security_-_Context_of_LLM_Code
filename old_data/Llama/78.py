
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
            raise ValueError("Cannot divide by zero!")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, Result: {result}")
        return result

    def get_history(self):
        
        return "\n".join(self.history)


def main():
    calculator = Calculator()

    while True:
        print("Calculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")
        print("6. Quit")

        choice = input("Choose an operation: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            try:
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(str(e))
        elif choice == "5":
            history = calculator.get_history()
            if not history:
                print("No calculations made yet.")
            else:
                print(history)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main()
