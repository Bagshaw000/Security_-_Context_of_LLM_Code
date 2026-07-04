
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}. Result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}. Result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}. Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"Divided {num1} by {num2}. Result: {result}")
        return result

    def get_history(self):
        
        return "\n".join(self.history)


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. View History")
        print("6. Quit")

        choice = input("Choose an operation (1-6): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == '1':
                result = calc.add(num1, num2)
            elif choice == '2':
                result = calc.subtract(num1, num2)
            elif choice == '3':
                result = calc.multiply(num1, num2)
            elif choice == '4':
                try:
                    result = calc.divide(num1, num2)
                except ValueError as e:
                    print(e)
                    continue

        elif choice == '5':
            print("\nCalculator History:")
            print(calc.get_history())

        elif choice == '6':
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
