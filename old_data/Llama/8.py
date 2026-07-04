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
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")
        
        choice = input("Choose an operation (1-5): ")

        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    print(f"Result: {calculator.add(num1, num2)}")
                    print("Calculator History:")
                    for entry in calculator.history:
                        print(entry)
                elif choice == '2':
                    print(f"Result: {calculator.subtract(num1, num2)}")
                    print("Calculator History:")
                    for entry in calculator.history:
                        print(entry)
                elif choice == '3':
                    print(f"Result: {calculator.multiply(num1, num2)}")
                    print("Calculator History:")
                    for entry in calculator.history:
                        print(entry)
                else:
                    print(f"Result: {calculator.divide(num1, num2)}")
                    print("Calculator History:")
                    for entry in calculator.history:
                        print(entry)

            except ValueError as e:
                print(str(e))

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()