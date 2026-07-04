
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
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero.")
        return num1 / num2


def main():
    calculator = Calculator()
    
    print("Simple Calculator Application")
    print("-------------------------------")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Choose an operation (1/2/3/4): ")

    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    if choice == '1':
        result = calculator.add(num1, num2)
        print(f"{num1} + {num2} = {result}")
    
    elif choice == '2':
        result = calculator.subtract(num1, num2)
        print(f"{num1} - {num2} = {result}")
    
    elif choice == '3':
        result = calculator.multiply(num1, num2)
        print(f"{num1} * {num2} = {result}")
    
    elif choice == '4':
        try:
            result = calculator.divide(num1, num2)
            print(f"{num1} / {num2} = {result}")
        except ValueError as e:
            print(str(e))
    
    else:
        print("Invalid choice. Please choose a valid operation.")


if __name__ == "__main__":
    main()
