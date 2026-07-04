
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
            raise ValueError("Cannot divide by zero")
        return num1 / num2


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

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.add(num1, num2)
            print(f"{num1} + {num2} = {result}")

        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")

        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calculator.multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")

        elif choice == "4":
            try:
                num1 = float(input("Enter the dividend: "))
                num2 = float(input("Enter the divisor: "))
                result = calculator.divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
