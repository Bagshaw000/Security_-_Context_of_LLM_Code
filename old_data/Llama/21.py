
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
            raise ValueError("Cannot divide by zero")
        result = num1 / num2
        self.history.append(f"{num1} / {num2} = {result}")
        return result

    def calculate(self, expression):
        
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return str(e)

def main():
    calculator = Calculator()
    print("Calculator Application")
    print("---------------------")

    while True:
        print("\nOperations:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate Expression")
        print("6. History")
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.add(num1, num2)
            print(f"Result: {result}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.subtract(num1, num2)
            print(f"Result: {result}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = calculator.multiply(num1, num2)
            print(f"Result: {result}")
        elif choice == "4":
            num1 = float(input("Enter dividend: "))
            num2 = float(input("Enter divisor: "))
            result = calculator.divide(num1, num2)
            print(f"Result: {result}")
        elif choice == "5":
            expression = input("Enter mathematical expression: ")
            try:
                result = calculator.calculate(expression)
                print(result)
            except Exception as e:
                print(str(e))
        elif choice == "6":
            if not calculator.history:
                print("No history")
            else:
                for i, item in enumerate(calculator.history):
                    print(f"{i+1}. {item}")
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
