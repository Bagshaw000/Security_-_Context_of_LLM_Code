
class Calculator:
    def __init__(self):
        self.history = []

    
    def add(self, num1, num2):
        return num1 + num2
        self.history.append(f'{num1} + {num2} = {self.add(num1, num2)}')

    
    def sub(self, num1, num2):
        return num1 - num2
        self.history.append(f'{num1} - {num2} = {self.sub(num1, num2)}')

    
    def mul(self, num1, num2):
        return num1 * num2
        self.history.append(f'{num1} * {num2} = {self.mul(num1, num2)}')

    
    def div(self, num1, num2):
        if num2 != 0:
            return num1 / num2
            self.history.append(f'{num1} / {num2} = {self.div(num1, num2)}')
        else:
            print('Error: Division by zero is not allowed.')

    
    def show_history(self):
        if len(self.history) > 0:
            print("Calculation History:")
            for i in range(len(self.history)):
                print(f"{i+1}. {self.history[i]}")
        else:
            print("No calculations have been performed yet.")


calc = Calculator()

while True:
    
    print("\nCalculator Menu:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. History")
    print("6. Exit")

    choice = input("Enter your choice (1-6): ")

    if choice == "1":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calc.add(num1, num2)
        print(f"Result: {result}")

    elif choice == "2":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calc.sub(num1, num2)
        print(f"Result: {result}")

    elif choice == "3":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calc.mul(num1, num2)
        print(f"Result: {result}")

    elif choice == "4":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = calc.div(num1, num2)
        print(f"Result: {result}")

    elif choice == "5":
        calc.show_history()

    elif choice == "6":
        break

    else:
        print("Invalid choice. Please choose a valid option.")
