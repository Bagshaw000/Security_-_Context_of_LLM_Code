
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, Result: {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"Multiplied {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 != 0:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")
            return result
        else:
            raise ValueError("Cannot divide by zero")

    def display_history(self):
        
        print("\nCalculator History:")
        for entry in self.history:
            print(entry)


def main():
    calc = Calculator()

    while True:
        print("\nCalculator Menu:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Display History")
        print("6. Quit")

        choice = input("Choose an operation: ")

        if choice == "6":
            break

        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if int(choice) % 2 == 0:
                print(f"{calc.add(num1, num2)}")
            else:
                print(f"{calc.subtract(num1, num2)}")

        elif choice == "5":
            calc.display_history()

        else:
            print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main()
