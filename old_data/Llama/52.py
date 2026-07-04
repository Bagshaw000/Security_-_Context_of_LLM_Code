
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        self.history.append(f"{num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        self.history.append(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        self.history.append(f"{num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        result = num1 / num2
        self.history.append(f"{num1} / {num2} = {result}")
        return result

    def calculate(self):
        
        print("\nCalculator History:")
        for i, entry in enumerate(self.history, start=1):
            print(f"{i}. {entry}")

def main():
    calc = Calculator()
    while True:
        print("\nOperations:")
        print("1. Add")
        print("2. Subtract")
        print("3. Multiply")
        print("4. Divide")
        print("5. Calculate History")
        print("6. Exit")

        choice = input("Choose an operation (1/2/3/4) or 5/6: ")

        if choice == "5":
            calc.calculate()
        elif choice in ["1", "2", "3", "4"]:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                if choice == "1":
                    print(f"Result: {calc.add(num1, num2)}")
                elif choice == "2":
                    print(f"Result: {calc.subtract(num1, num2)}")
                elif choice == "3":
                    print(f"Result: {calc.multiply(num1, num2)}")
                elif choice == "4":
                    try:
                        calc.divide(num1, num2)
                    except ValueError as e:
                        print(e)
            except ValueError as e:
                print(e)
        elif choice == "6":
            break
        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    main()
