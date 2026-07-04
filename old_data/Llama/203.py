


class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"Result: {num1} + {num2} = {result}")
        self.history.append((f"{num1} + {num2}", result))
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"Result: {num1} - {num2} = {result}")
        self.history.append((f"{num1} - {num2}", result))
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"Result: {num1} * {num2} = {result}")
        self.history.append((f"{num1} * {num2}", result))
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            print("Error: Division by zero")
        else:
            result = num1 / num2
            print(f"Result: {num1} / {num2} = {result}")
            self.history.append((f"{num1} / {num2}", result))
        return result

    def display_history(self):
        
        if not self.history:
            print("No operations performed")
        else:
            for i, entry in enumerate(self.history):
                print(f"Operation {i+1}: {entry[0]} = {entry[1]}")


def main():
    calculator = Calculator()
    
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                print(calculator.add(num1, num2))
            elif choice == "2":
                print(calculator.subtract(num1, num2))
            elif choice == "3":
                print(calculator.multiply(num1, num2))
            elif choice == "4":
                print(calculator.divide(num1, num2))

        elif choice == "5":
            calculator.display_history()

        elif choice == "6":
            break

        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
