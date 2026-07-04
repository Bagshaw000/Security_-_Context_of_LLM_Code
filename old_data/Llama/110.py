
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
        if num2 != 0:
            return num1 / num2
        else:
            raise ValueError("Cannot divide by zero")

    def calculate(self):
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Clear History")
            print("6. Exit")

            choice = input("Choose an operation (1/2/3/4) or enter the number of a saved calculation: ")

            if choice == "1":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.add(num1, num2)
                print(f"{num1} + {num2} = {result}")
                self.history.append((f"{num1} + {num2}", result))

            elif choice == "2":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
                self.history.append((f"{num1} - {num2}", result))

            elif choice == "3":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = self.multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
                self.history.append((f"{num1} * {num2}", result))

            elif choice == "4":
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                try:
                    result = self.divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                    self.history.append((f"{num1} / {num2}", result))
                except ValueError as e:
                    print(e)

            elif choice == "5":
                print("\nSaved Calculations:")
                for i, calc in enumerate(self.history):
                    print(f"{i+1}. {calc[0]} = {calc[1]}")

            elif choice == "6":
                break

            else:
                print("Invalid choice. Please choose a valid option.")

    def run(self):
        self.calculate()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
