
def add(x, y):
    
    return x + y


def subtract(x, y):
    
    return x - y


def multiply(x, y):
    
    return x * y


def divide(x, y):
    
    if y == 0:
        raise ValueError("Cannot divide by zero!")
    return x / y


def main():
    print("Calculator Application")
    print("---------------------")

    while True:
        
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1/2/3/4) or 5 to quit: ")

        if choice == '5':
            break

        try:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))
        except ValueError:
            print("Invalid input! Please enter a valid number.")
            continue

        if choice == '1':
            result = add(num1, num2)
            print(f"{num1} + {num2} = {result}")
        elif choice == '2':
            result = subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")
        elif choice == '3':
            result = multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")
        elif choice == '4':
            try:
                result = divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(str(e))

if __name__ == "__main__":
    main()
