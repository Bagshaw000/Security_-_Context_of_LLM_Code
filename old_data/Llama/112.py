
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

def main():
    calculator = Calculator()

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")
        print("6. Quit")

        choice = input("Enter your choice (1-6): ")

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
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = calculator.divide(num1, num2)
                print(f"Result: {result}")
            except ValueError as e:
                print(e)

        elif choice == "5":
            if calculator.history:
                print("\nHistory:")
                for i, entry in enumerate(calculator.history):
                    print(f"{i+1}. {entry}")
            else:
                print("No calculations history")

        elif choice == "6":
            print("\nGoodbye!")
            break

        else:
            print("\nInvalid choice. Please choose again.")

if __name__ == "__main__":
    main()
