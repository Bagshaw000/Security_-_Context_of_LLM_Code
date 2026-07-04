import math

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
            return "Error! Division by zero is not allowed."

    def square_root(self, num):
        try:
            return math.sqrt(num)
        except ValueError:
            return "Error! Input must be a non-negative number."

    def power(self, base, exponent):
        return base ** exponent

def main():
    calc = Calculator()
    
    while True:
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Square Root")
        print("6. Power")
        print("7. Quit")
        
        choice = input("Enter your choice (1-7): ")
        
        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            
            if choice == '1':
                print(f"{num1} + {num2} = {calc.add(num1, num2)}")
            elif choice == '2':
                print(f"{num1} - {num2} = {calc.subtract(num1, num2)}")
            elif choice == '3':
                print(f"{num1} * {num2} = {calc.multiply(num1, num2)}")
            elif choice == '4':
                if num2 != 0:
                    print(f"{num1} / {num2} = {calc.divide(num1, num2)}")
                else:
                    print(calc.divide(num1, num2))
        elif choice in ('5', '6'):
            num = float(input("Enter a number: "))
            
            if choice == '5':
                print(f"√{num} = {calc.square_root(num)}")
            elif choice == '6':
                base = float(input("Enter the base: "))
                exponent = float(input("Enter the exponent: "))
                print(f"{base}^{exponent} = {calc.power(base, exponent)}")
        elif choice == '7':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()