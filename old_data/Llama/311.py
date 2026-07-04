
import math

def add(x, y):
    
    return x + y

def subtract(x, y):
    
    return x - y

def multiply(x, y):
    
    return x * y

def divide(x, y):
    
    if y != 0:
        return x / y
    else:
        print("Error: Division by zero is not allowed")
        return None

def exponentiation(x, y):
    
    return math.pow(x, y)

def square_root(x):
    
    if x >= 0:
        return math.sqrt(x)
    else:
        print("Error: Square root of negative numbers is not defined")
        return None

def main():
    print("Calculator Application")

    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exponentiation")
        print("6. Square Root")
        print("7. Quit")

        choice = input("Enter your choice (1-7): ")

        if choice == "1":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"Result: {add(num1, num2)}")
        elif choice == "2":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"Result: {subtract(num1, num2)}")
        elif choice == "3":
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            print(f"Result: {multiply(num1, num2)}")
        elif choice == "4":
            num1 = float(input("Enter dividend: "))
            num2 = float(input("Enter divisor: "))
            print(f"Result: {divide(num1, num2)}")
        elif choice == "5":
            num1 = float(input("Enter base number: "))
            num2 = float(input("Enter exponent: "))
            print(f"Result: {exponentiation(num1, num2)}")
        elif choice == "6":
            num = float(input("Enter a number: "))
            print(f"Result: {square_root(num)}")
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
