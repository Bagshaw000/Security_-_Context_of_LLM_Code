
import math

def add(num1, num2):
    
    return num1 + num2

def subtract(num1, num2):
    
    return num1 - num2

def multiply(num1, num2):
    
    return num1 * num2

def divide(num1, num2):
    
    if num2 == 0:
        raise ValueError("Cannot divide by zero")
    return num1 / num2

def square_root(num):
    
    try:
        return math.sqrt(num)
    except ValueError as e:
        print(e)

def log(num):
    
    try:
        if num <= 0:
            raise ValueError("Logarithm is not defined for non-positive numbers")
        return math.log(num)
    except ValueError as e:
        print(e)

def main():
    while True:
        
        print("\nCalculator Menu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Square Root")
        print("6. Logarithm")
        print("7. Quit")

        
        choice = input("\nEnter your choice (1-7): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == "1":
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == "2":
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == "3":
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            else:
                try:
                    print(f"{num1} / {num2} = {divide(num1, num2)}")
                except ValueError as e:
                    print(e)
        elif choice == "5":
            num = float(input("Enter number: "))
            print(f"Square root of {num} is {square_root(num)}")
        elif choice == "6":
            num = float(input("Enter number: "))
            try:
                print(f"log({num}) = {log(num)}")
            except ValueError as e:
                print(e)
        elif choice == "7":
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
