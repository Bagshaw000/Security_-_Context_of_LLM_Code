
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
            raise ValueError("Cannot divide by zero!")
        return num1 / num2

    def calculate_history(self):
        
        for i, (operation, num1, num2, result) in enumerate(self.history):
            print(f"Calculation {i+1}: {operation}({num1}, {num2}) = {result}")

    def run(self):
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Choose an operation (1-5): ")

            if choice == "1":
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                result = self.add(num1, num2)
                print(f"Result: {result}")
                self.history.append(("add", num1, num2, result))

            elif choice == "2":
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                result = self.subtract(num1, num2)
                print(f"Result: {result}")
                self.history.append(("subtract", num1, num2, result))

            elif choice == "3":
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                result = self.multiply(num1, num2)
                print(f"Result: {result}")
                self.history.append(("multiply", num1, num2, result))

            elif choice == "4":
                try:
                    num1 = float(input("Enter the first number: "))
                    num2 = float(input("Enter the second number: "))
                    result = self.divide(num1, num2)
                    print(f"Result: {result}")
                    self.history.append(("divide", num1, num2, result))
                except ValueError as e:
                    print(e)

            elif choice == "5":
                print("\nExiting calculator. Calculation history:")
                self.calculate_history()
                break

            else:
                print("Invalid choice! Please choose a valid operation.")


if __name__ == "__main__":
    calc = Calculator()
    calc.run()
