def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    return a / b

def main():
    print("Welcome to the calculator!")
    while True:
        print("Please select an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")
        
        choice = input("Enter your choice (1-5): ")
        
        if choice == '5':
            print("Exiting the calculator...")
            break
        
        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))
        
        if choice == '1':
            result = add(num1, num2)
            print(f"The result is: {result}")
        elif choice == '2':
            result = subtract(num1, num2)
            print(f"The result is: {result}")
        elif choice == '3':
            result = multiply(num1, num2)
            print(f"The result is: {result}")
        elif choice == '4':
            if num2 == 0:
                print("Error: Cannot divide by zero")
            else:
                result = divide(num1, num2)
                print(f"The result is: {result}")
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()