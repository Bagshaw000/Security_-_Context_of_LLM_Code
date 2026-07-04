
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
            raise ValueError("Cannot divide by zero!")
        return num1 / num2

def main():
    calculator = Calculator()
    
    print("Calculator Application")
    print("--------------------")

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            print("\nGoodbye!")
            break

        elif choice in ["1", "2", "3"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                result = calculator.add(num1, num2)
            elif choice == "2":
                result = calculator.subtract(num1, num2)
            elif choice == "3":
                result = calculator.multiply(num1, num2)

            print(f"\nResult: {result}")

        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))

            try:
                result = calculator.divide(num1, num2)
                print(f"\nResult: {result}")
            except ValueError as e:
                print(e)

        else:
            print("\nInvalid choice. Please choose again.")

if __name__ == "__main__":
    main()
