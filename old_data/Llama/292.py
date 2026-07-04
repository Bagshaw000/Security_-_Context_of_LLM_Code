
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
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Choose an operation (1-5): ")

            if choice in ['1', '2', '3', '4']:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if choice == '1':
                    result = self.add(num1, num2)
                elif choice == '2':
                    result = self.subtract(num1, num2)
                elif choice == '3':
                    result = self.multiply(num1, num2)
                else:
                    try:
                        result = self.divide(num1, num2)
                    except ValueError as e:
                        print(e)
                        continue

                print(f"{num1} {['+', '-', '*', '/'][int(choice) - 1]} {num2} = {result}")

                
                self.history.append((f"{num1} {['+', '-', '*', '/'][int(choice) - 1]} {num2}", result))

            elif choice == '5':
                print("Goodbye!")
                break

            else:
                print("Invalid choice. Please choose a valid option.")

    def view_history(self):
        
        if not self.history:
            print("No calculations yet.")
            return

        for i, (calculation, result) in enumerate(self.history, start=1):
            print(f"\nCalculation {i}:")
            print(calculation)
            print(f"Result: {result}")


if __name__ == "__main__":
    calculator = Calculator()
    while True:
        print("\nCalculator Menu:")
        print("1. Perform calculation")
        print("2. View calculation history")
        print("3. Quit")

        choice = input("Choose an option (1-3): ")

        if choice == '1':
            calculator.calculate()
        elif choice == '2':
            calculator.view_history()
        else:
            print("Goodbye!")
            break
