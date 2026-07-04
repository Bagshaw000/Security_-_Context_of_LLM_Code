
class Calculator:
    def __init__(self):
        self.history = []

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

    def history(self):
        
        return self.history

def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. History")

        choice = input("Choose an option: ")

        if choice == '5':
            history = calc.history()
            print("\nHistory:")
            for i, item in enumerate(history):
                print(f"{i+1}. {item}")
        elif choice in ['1', '2', '3']:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if choice == '1':
                    result = calc.add(num1, num2)
                    print(f"\nResult of {num1} + {num2} = {result}")
                    calc.history.append(f"{num1} + {num2} = {result}")
                elif choice == '2':
                    result = calc.subtract(num1, num2)
                    print(f"\nResult of {num1} - {num2} = {result}")
                    calc.history.append(f"{num1} - {num2} = {result}")
                else:
                    result = calc.multiply(num1, num2)
                    print(f"\nResult of {num1} * {num2} = {result}")
                    calc.history.append(f"{num1} * {num2} = {result}")
            except ValueError as e:
                print(e)

        elif choice == '4':
            try:
                num1 = float(input("Enter the dividend: "))
                num2 = float(input("Enter the divisor: "))

                if num2 == 0:
                    raise ValueError("Cannot divide by zero")

                result = calc.divide(num1, num2)
                print(f"\nResult of {num1} / {num2} = {result}")
                calc.history.append(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
