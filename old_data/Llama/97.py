
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        self.history.append((f"{num1} + {num2}", result))
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        self.history.append((f"{num1} - {num2}", result))
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        self.history.append((f"{num1} * {num2}", result))
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
        self.history.append((f"{num1} / {num2}", result))
        return result

    def display_history(self):
        
        for i, (calculation, result) in enumerate(self.history):
            print(f"Calculation {i+1}: {calculation} = {result}")


def main():
    calculator = Calculator()

    while True:
        print("\nOptions:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        option = input("Choose an option: ")

        if option == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.add(num1, num2)
        elif option == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.subtract(num1, num2)
        elif option == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            calculator.multiply(num1, num2)
        elif option == "4":
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                result = calculator.divide(num1, num2)
            except ValueError as e:
                print(e)
                continue
        elif option == "5":
            calculator.display_history()
        elif option == "6":
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
