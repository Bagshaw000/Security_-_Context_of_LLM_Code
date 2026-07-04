


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
        self.history.append(f"Multiplied {num1} and {num2}, result = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}, result = {result}")
        return result

    def print_history(self):
        
        for i, entry in enumerate(self.history, start=1):
            print(f"{i}. {entry}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nCalculator Application")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Print History")
        print("6. Quit")

        choice = input("Choose an operation (1/2/3/4/5/6): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                print(f"Result: {calculator.add(num1, num2)}")
            elif choice == "2":
                print(f"Result: {calculator.subtract(num1, num2)}")
            elif choice == "3":
                print(f"Result: {calculator.multiply(num1, num2)}")
            elif choice == "4":
                try:
                    print(f"Result: {calculator.divide(num1, num2)}")
                except ValueError as e:
                    print(str(e))
        elif choice == "5":
            calculator.print_history()
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()
