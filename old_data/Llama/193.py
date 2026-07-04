
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
            print("Error! Division by zero is not allowed.")
            return None

    
    def square(self, num):
        return num ** 2

    
    def cube(self, num):
        return num ** 3


def main():
    calc = Calculator()
    
    while True:
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Square of a number")
        print("6. Cube of a number")
        print("7. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.add(num1, num2)
            print(f"{num1} + {num2} = {result}")

        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")

        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = calc.multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")

        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))
            result = calc.divide(num1, num2)
            if isinstance(result, (int, float)):
                print(f"{num1} / {num2} = {result}")

        elif choice == "5":
            num = float(input("Enter a number: "))
            result = calc.square(num)
            print(f"Square of {num} = {result}")

        elif choice == "6":
            num = float(input("Enter a number: "))
            result = calc.cube(num)
            print(f"Cube of {num} = {result}")

        elif choice == "7":
            break

        else:
            print("Invalid option. Please choose again.")


if __name__ == "__main__":
    main()
