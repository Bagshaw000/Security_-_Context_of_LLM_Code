
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        self.history.append(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"Result: {num1} × {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error! Division by zero is not allowed.")
            return None
        result = num1 / num2
        print(f"Result: {num1} ÷ {num2} = {result}")
        self.history.append(f"{num1} ÷ {num2} = {result}")
        return result

    def calculate(self):
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Enter your choice (1-5): ")

            if choice == "5":
                break
            elif choice not in ["1", "2", "3", "4"]:
                print("Invalid choice! Please try again.")
                continue

            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                self.add(num1, num2)
            elif choice == "2":
                self.subtract(num1, num2)
            elif choice == "3":
                self.multiply(num1, num2)
            elif choice == "4":
                result = self.divide(num1, num2)
                if result is not None:
                    print(f"Result: {num1} ÷ {num2} = {result}")

        
        print("\nCalculator History:")
        for i, entry in enumerate(self.history):
            print(f"{i+1}. {entry}")


if __name__ == "__main__":
    calc = Calculator()
    calc.calculate()
