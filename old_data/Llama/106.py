
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
            raise ValueError("Cannot divide by zero.")
        return num1 / num2

    def calculate(self):
        
        print("Choose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == '1':
                result = self.add(num1, num2)
                print(f"{num1} + {num2} = {result}")
                self.history.append(f"Addition of {num1} and {num2}, result is {result}")

            elif choice == '2':
                result = self.subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
                self.history.append(f"Subtraction of {num1} and {num2}, result is {result}")

            elif choice == '3':
                result = self.multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
                self.history.append(f"Multiplication of {num1} and {num2}, result is {result}")

            elif choice == '4':
                try:
                    result = self.divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                    self.history.append(f"Division of {num1} and {num2}, result is {result}")
                except ValueError as e:
                    print(str(e))

        else:
            print("Invalid choice. Please choose a valid option.")

    def display_history(self):
        
        if not self.history:
            print("No calculations have been performed yet.")
        else:
            for i, calculation in enumerate(self.history):
                print(f"Calculation {i+1}: {calculation}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Application")
        print("---------------------")
        print("1. Perform a calculation")
        print("2. Display calculation history")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ")

        if choice == '1':
            calculator.calculate()
        elif choice == '2':
            calculator.display_history()
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please choose a valid option.")


if __name__ == "__main__":
    main()
