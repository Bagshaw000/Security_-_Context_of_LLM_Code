
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
    
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1/2/3/4/5): ")

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    result = calculator.add(num1, num2)
                elif choice == '2':
                    result = calculator.subtract(num1, num2)
                elif choice == '3':
                    result = calculator.multiply(num1, num2)
                else:
                    result = calculator.divide(num1, num2)

                print(f"{num1} {('+' if choice == '1' else '-'}' {num2} = {result})")
            except ValueError as e:
                print(str(e))
        elif choice == '5':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main() 