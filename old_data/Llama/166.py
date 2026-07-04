

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"Result: {result}")
        self.history.append(f"{num1} + {num2} = {result}")

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"Result: {result}")
        self.history.append(f"{num1} - {num2} = {result}")

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"Result: {result}")
        self.history.append(f"{num1} * {num2} = {result}")

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error! Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"Result: {result}")
            self.history.append(f"{num1} / {num2} = {result}")


def main():
    calculator = Calculator()
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                calculator.add(num1, num2)
            elif choice == "2":
                calculator.subtract(num1, num2)
            elif choice == "3":
                calculator.multiply(num1, num2)
            else:
                calculator.divide(num1, num2)

        print("\nCalculator History:")
        for i, entry in enumerate(calculator.history):
            print(f"{i+1}. {entry}")


if __name__ == "__main__":
    main()
