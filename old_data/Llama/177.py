

def add(num1, num2):
    
    return num1 + num2

def subtract(num1, num2):
    
    return num1 - num2

def multiply(num1, num2):
    
    return num1 * num2

def divide(num1, num2):
    
    if num2 == 0:
        raise ValueError("Cannot divide by zero!")
    return num1 / num2

def calculator():
    print("Calculator Application")
    while True:
        print("\n1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("\nEnter your choice (1-5): ")

        if choice in ('1', '2', '3', '4'):
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            if choice == '1':
                result = add(num1, num2)
                print(f"{num1} + {num2} = {result}")
            elif choice == '2':
                result = subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
            elif choice == '3':
                result = multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
            else:
                result = divide(num1, num2)
                print(f"{num1} / {num2} = {result}")

        elif choice == '5':
            print("Exiting calculator. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    calculator()
