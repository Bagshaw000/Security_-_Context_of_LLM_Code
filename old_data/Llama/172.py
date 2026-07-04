class Calculator:
    def __init__(self):
        pass

    def add(self, num1, num2):
        return num1 + num2

    def subtract(self, num1, num2):
        return num1 - num2

    def multiply(self, num1, num2):
        return num1 * num2

    def divide(self, num1, num2):
        if num2 != 0:
            return num1 / num2
        else:
            return "Error: Division by zero is not allowed"

    def calculate_expression(self, expression):
        try:
            result = eval(expression)
            return f"{expression} = {result}"
        except Exception as e:
            return str(e)

def main():
    calculator = Calculator()
    while True:
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Calculate Expression")
        print("6. Quit")
        
        choice = input("Choose an operation: ")
        
        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            if choice == "1":
                print(f"{num1} + {num2} = {calculator.add(num1, num2)}")
            elif choice == "2":
                print(f"{num1} - {num2} = {calculator.subtract(num1, num2)}")
            elif choice == "3":
                print(f"{num1} * {num2} = {calculator.multiply(num1, num2)}")
            elif choice == "4":
                print(f"{num1} / {num2} = {calculator.divide(num1, num2)}")
        
        elif choice == "5":
            expression = input("Enter an expression: ")
            print(calculator.calculate_expression(expression))
        
        elif choice == "6":
            break
        
        else:
            print("Invalid choice. Please choose a valid operation.")

if __name__ == "__main__":
    main()