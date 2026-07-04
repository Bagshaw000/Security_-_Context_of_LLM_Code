

def add(x, y):
    
    return x + y

def subtract(x, y):
    
    return x - y

def multiply(x, y):
    
    return x * y

def divide(x, y):
    
    if y == 0:
        raise ValueError("Cannot divide by zero")
    return x / y

def calculator():
    print("Calculator Application")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    choice = input("Choose an operation (1/2/3/4): ")

    if choice == "1":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = add(num1, num2)
        print(f"Result: {result}")

    elif choice == "2":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = subtract(num1, num2)
        print(f"Result: {result}")

    elif choice == "3":
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))
        result = multiply(num1, num2)
        print(f"Result: {result}")

    elif choice == "4":
        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
            result = divide(num1, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(str(e))

def main():
    while True:
        calculator()
        cont = input("Do you want to perform another calculation? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    main()
