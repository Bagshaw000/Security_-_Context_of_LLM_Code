
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

    def calculate(self):
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Choose an operation: ")

            if choice == "5":
                break

            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            operations = {
                "1": self.add,
                "2": self.subtract,
                "3": self.multiply,
                "4": self.divide
            }

            try:
                result = operations[choice](num1, num2)
                print(f"{num1} {choice.upper()} {num2} = {result}")
                self.history.append((f"{num1} {choice.upper()} {num2}", result))
            except ValueError as e:
                print(str(e))

    def view_history(self):
        
        if not self.history:
            print("No calculations performed.")
        else:
            print("\nCalculation History:")
            for i, (calculation, result) in enumerate(self.history):
                print(f"{i+1}. {calculation} = {result}")


def main():
    calculator = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Calculate a value")
        print("2. View calculation history")
        print("3. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            calculator.calculate()
        elif choice == "2":
            calculator.view_history()
        elif choice == "3":
            break
        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
