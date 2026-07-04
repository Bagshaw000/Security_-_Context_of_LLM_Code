
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
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"{num1} / {num2} = {result}")
        return result

    def print_history(self):
        
        for i, entry in enumerate(self.history):
            print(f"{i+1}. {entry}")


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Print History")
        print("6. Quit")

        choice = input("Choose an operation: ")

        if choice == "6":
            break

        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == "1":
            result = calc.add(num1, num2)
        elif choice == "2":
            result = calc.subtract(num1, num2)
        elif choice == "3":
            result = calc.multiply(num1, num2)
        elif choice == "4":
            try:
                result = calc.divide(num1, num2)
            except ValueError as e:
                print(e)
                continue
        else:
            print("Invalid choice. Please choose a valid operation.")
            continue

        print(f"Result: {result}\n")

    calc.print_history()


if __name__ == "__main__":
    main()
