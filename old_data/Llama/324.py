
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, result is {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, result is {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, result is {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result is {result}")
        return result

    def print_history(self):
        
        for i, item in enumerate(self.history, start=1):
            print(f"{i}. {item}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nMenu:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Print History")
        print("6. Quit")

        choice = input("Choose an operation: ")

        if choice == "6":
            break

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            continue

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
            calculator.print_history()
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
