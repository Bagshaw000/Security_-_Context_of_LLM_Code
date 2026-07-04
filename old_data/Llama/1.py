

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

    def calculate(self):
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Calculate History")
            print("6. Quit")

            choice = input("Choose an operation (1-6): ")

            if choice == "1":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.add(num1, num2)
                print(f"Result: {result}")

            elif choice == "2":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.subtract(num1, num2)
                print(f"Result: {result}")

            elif choice == "3":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.multiply(num1, num2)
                print(f"Result: {result}")

            elif choice == "4":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                try:
                    result = self.divide(num1, num2)
                    print(f"Result: {result}")
                except ValueError as e:
                    print(e)

            elif choice == "5":
                if not self.history:
                    print("No calculations performed yet.")
                else:
                    for i, calc in enumerate(self.history):
                        print(f"{i+1}. {calc}")

            elif choice == "6":
                break

            else:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    calculator = Calculator()
    calculator.calculate()
