
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

    def display_history(self):
        print("\nCalculator History:")
        for entry in self.history:
            print(entry)


def main():
    calculator = Calculator()

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display history")
        print("6. Quit")

        choice = input("Enter your choice (1/2/3/4/5/6): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == '1':
                print(f"{num1} + {num2} = {calculator.add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {calculator.subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {calculator.multiply(num1, num2)}")
            elif choice == '4':
                try:
                    calculator.divide(num1, num2)
                except ValueError as e:
                    print(e)

        elif choice == '5':
            calculator.display_history()

        elif choice == '6':
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
