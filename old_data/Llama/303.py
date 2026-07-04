
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
            raise ValueError("Error: Division by zero is not allowed")
        return num1 / num2

    def calculate(self):
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")
            
            choice = input("\nEnter your choice (1-5): ")
            
            if choice in ['1', '2', '3', '4']:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))

                if choice == '1':
                    print(f"{num1} + {num2} = {self.add(num1, num2)}")
                elif choice == '2':
                    print(f"{num1} - {num2} = {self.subtract(num1, num2)}")
                elif choice == '3':
                    print(f"{num1} * {num2} = {self.multiply(num1, num2)}")
                else:
                    try:
                        print(f"{num1} / {num2} = {self.divide(num1, num2)}")
                    except ValueError as e:
                        print(str(e))
            elif choice == '5':
                print("\nExiting calculator. Goodbye!")
                break
            else:
                print("Invalid choice. Please choose a valid option.")

    def display_history(self):
        if len(self.history) > 0:
            print("\nCalculator History:")
            for i, operation in enumerate(self.history):
                print(f"{i+1}. {operation}")
        else:
            print("\nNo calculations history yet.")


def main():
    calculator = Calculator()

    while True:
        print("\nWelcome to the Calculator Application!")
        print("Please select an option:")
        print("1. Start Calculating")
        print("2. View Calculations History")
        print("3. Exit")

        choice = input("\nEnter your choice (1-3): ")

        if choice == '1':
            calculator.calculate()
        elif choice == '2':
            calculator.display_history()
        elif choice == '3':
            print("Exiting application. Goodbye!")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
