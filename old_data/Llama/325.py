
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
        self.history.append(f"Multiply {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")
            return result
        else:
            raise ValueError("Cannot divide by zero")

    def calculate(self, operation, *args):
        
        operations = {
            "+": self.add,
            "-": self.subtract,
            "*": self.multiply,
            "/": self.divide
        }
        if operation in operations:
            return operations[operation](*args)
        else:
            raise ValueError("Invalid operation")

    def print_history(self):
        
        for i, operation in enumerate(self.history):
            print(f"{i+1}. {operation}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate with custom operation")
        print("6. Print History")
        print("7. Quit")

        choice = input("Enter your choice: ")

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
                print(e)
        elif choice == "5":
            operation = input("Enter the operation (+, -, *, /): ")
            args = [float(x) for x in input("Enter numbers (separated by space): ").split()]
            result = calculator.calculate(operation, *args)
            print(f"Result: {result}")
        elif choice == "6":
            calculator.print_history()
        elif choice == "7":
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
