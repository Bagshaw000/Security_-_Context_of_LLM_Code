
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, result = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, result = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiply {num1} and {num2}, result = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result = {result}")
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
        
        choice = input("Choose an operation: ")
        
        if choice == "5":
            break
        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice. Please try again.")
            continue
        
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        if choice == "1":
            result = calculator.add(num1, num2)
        elif choice == "2":
            result = calculator.subtract(num1, num2)
        elif choice == "3":
            result = calculator.multiply(num1, num2)
        else:
            try:
                result = calculator.divide(num1, num2)
            except ValueError as e:
                print(str(e))
                continue
        
        print(f"Result: {result}")
        
        print("\nCalculation History:")
        for i, history in enumerate(calculator.get_history(), start=1):
            print(f"{i}. {history}")


if __name__ == "__main__":
    main()
