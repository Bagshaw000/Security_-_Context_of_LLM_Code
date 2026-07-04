
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
            print("\nCalculator Application")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Choose an operation (1/2/3/4/5): ")

            if choice == "5":
                break

            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                result = self.add(num1, num2)
                print(f"{num1} + {num2} = {result}")
                self.history.append((f"{num1} + {num2}", result))

            elif choice == "2":
                result = self.subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
                self.history.append((f"{num1} - {num2}", result))

            elif choice == "3":
                result = self.multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
                self.history.append((f"{num1} * {num2}", result))

            elif choice == "4":
                try:
                    result = self.divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                    self.history.append((f"{num1} / {num2}", result))
                except ValueError as e:
                    print(e)

            print("\nCalculator History:")
            for entry in self.history:
                print(f"{entry[0]}: {entry[1]}")

if __name__ == "__main__":
    calculator = Calculator()
    calculator.calculate()
