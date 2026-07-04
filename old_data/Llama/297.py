
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"Result: {result}")
        self.history.append(f"{num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"Result: {result}")
        self.history.append(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"Result: {result}")
        self.history.append(f"{num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        result = num1 / num2
        print(f"Result: {result}")
        self.history.append(f"{num1} / {num2} = {result}")
        return result

    def display_history(self):
        
        print("\nCalculation History:")
        for i, entry in enumerate(self.history):
            print(f"{i+1}. {entry}")


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "6":
            break
        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice! Please try again.")
            continue

        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        if choice == "1":
            result = calc.add(num1, num2)
        elif choice == "2":
            result = calc.subtract(num1, num2)
        elif choice == "3":
            result = calc.multiply(num1, num2)
        elif choice == "4":
            try:
                result = calc.divide(num1, num2)
            except ValueError as e:
                print(str(e))
                continue

        print("\nResult: ", end="")
        print(f"{num1} {'+' if choice == '1' else '-' if choice == '2' else '*' if choice == '3' else '/' if choice == '4' else ''}{num2}")

    calc.display_history()


if __name__ == "__main__":
    main()
