
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        self.history.append((f"Addition", f"{num1} + {num2} = {result}"))
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        self.history.append((f"Subtraction", f"{num1} - {num2} = {result}"))
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append((f"Multiplication", f"{num1} * {num2} = {result}"))
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error: Division by zero is not allowed.")
        else:
            result = num1 / num2
            print(f"{num1} / {num2} = {result}")
            self.history.append((f"Division", f"{num1} / {num2} = {result}"))
        return result

    def calculate(self):
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. History")
            print("6. Exit")

            choice = input("Enter your choice (1-6): ")

            if choice in ["1", "2", "3", "4"]:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if choice == "1":
                    print(self.add(num1, num2))
                elif choice == "2":
                    print(self.subtract(num1, num2))
                elif choice == "3":
                    print(self.multiply(num1, num2))
                elif choice == "4":
                    print(self.divide(num1, num2))

            elif choice == "5":
                if self.history:
                    for i, (op, result) in enumerate(self.history):
                        print(f"{i+1}. {op}: {result}")
                else:
                    print("No calculation history.")

            elif choice == "6":
                break

            else:
                print("Invalid choice. Please try again.")

if __name__ == "__main__":
    calculator = Calculator()
    calculator.calculate()
