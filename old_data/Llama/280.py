
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result: {result}")
        return result

    def get_history(self):
        
        return self.history


def main():
    calculator = Calculator()
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1-5): ")

        if choice == "5":
            break

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if choice == "1":
            result = calculator.add(num1, num2)
        elif choice == "2":
            result = calculator.subtract(num1, num2)
        elif choice == "3":
            result = calculator.multiply(num1, num2)
        elif choice == "4":
            try:
                result = calculator.divide(num1, num2)
            except ValueError as e:
                print(e)
                continue
        else:
            print("Invalid choice!")
            continue

        print(f"Result: {result}")
        print("History:")
        for entry in calculator.get_history():
            print(entry)


if __name__ == "__main__":
    main()
