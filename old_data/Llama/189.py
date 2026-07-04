class Calculator:
    def add(self, num1, num2):
        return num1 + num2

    def subtract(self, num1, num2):
        return num1 - num2

    def multiply(self, num1, num2):
        return num1 * num2

    def divide(self, num1, num2):
        if num2 == 0:
            return "Error: Division by zero is not allowed"
        else:
            return num1 / num2


def main():
    calculator = Calculator()

    while True:
        print("Calculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                print(f"Result: {calculator.add(num1, num2)}")
            elif choice == "2":
                print(f"Result: {calculator.subtract(num1, num2)}")
            elif choice == "3":
                print(f"Result: {calculator.multiply(num1, num2)}")
            elif choice == "4":
                result = calculator.divide(num1, num2)
                if isinstance(result, str):
                    print(result)
                else:
                    print(f"Result: {result}")
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()