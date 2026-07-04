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
        print("Select an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice == '1':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = add(num1, num2)
            print(f"The result is: {result}")
        elif choice == '2':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = subtract(num1, num2)
            print(f"The result is: {result}")
        elif choice == '3':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = multiply(num1, num2)
            print(f"The result is: {result}")
        elif choice == '4':
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = divide(num1, num2)
            print(f"The result is: {result}")
        elif choice == '5':
            print("Exiting the calculator...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()