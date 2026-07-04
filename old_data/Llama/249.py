
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}. Result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}. Result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}. Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}. Result: {result}")
            return result
        else:
            print("Error: Division by zero is not allowed.")
            return None

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
        print("5. History")
        print("6. Quit")

        choice = input("Enter your choice: ")

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
            result = calculator.divide(num1, num2)
            if result is not None:
                print(f"Result: {result}")
        elif choice == "5":
            history = calculator.get_history()
            for i, item in enumerate(history):
                print(f"{i+1}. {item}")
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
