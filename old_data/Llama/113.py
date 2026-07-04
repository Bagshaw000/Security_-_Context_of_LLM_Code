
class Calculator:
    def __init__(self):
        pass

    def add(self, num1, num2):
        
        return num1 + num2

    def subtract(self, num1, num2):
        
        return num1 - num2

    def multiply(self, num1, num2):
        
        return num1 * num2

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Choose an operation (1-5): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == '1':
                print(f"Result: {calculator.add(num1, num2)}")
            elif choice == '2':
                print(f"Result: {calculator.subtract(num1, num2)}")
            elif choice == '3':
                print(f"Result: {calculator.multiply(num1, num2)}")
            elif choice == '4':
                try:
                    print(f"Result: {calculator.divide(num1, num2)}")
                except ValueError as e:
                    print(e)
        elif choice == '5':
            print("Exiting the calculator. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main()
