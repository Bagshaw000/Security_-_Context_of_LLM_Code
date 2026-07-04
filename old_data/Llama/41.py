

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        return result

    def calculate(self):
        
        while True:
            print("\nChoose an operation:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Enter your choice (1/2/3/4/5): ")

            if choice == "5":
                break

            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                print(f"{num1} + {num2} = {self.add(num1, num2)}")
            elif choice == "2":
                print(f"{num1} - {num2} = {self.subtract(num1, num2)}")
            elif choice == "3":
                print(f"{num1} * {num2} = {self.multiply(num1, num2)}")
            elif choice == "4":
                try:
                    print(f"{num1} / {num2} = {self.divide(num1, num2)}")
                except ValueError as e:
                    print(str(e))
            else:
                print("Invalid choice. Please choose again.")

            self.history.append((f"{num1} {choice} {num2}", f"{num1} {choice} {num2} = {self.evaluate(choice, num1, num2)}"))

    def evaluate(self, operation, num1, num2):
        
        operations = {
            "addition": self.add,
            "subtraction": self.subtract,
            "multiplication": self.multiply,
            "division": self.divide
        }

        return operations[operation](num1, num2)


if __name__ == "__main__":
    calculator = Calculator()
    calculator.calculate()
