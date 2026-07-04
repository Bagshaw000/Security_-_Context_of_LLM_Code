

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

def calculator():
    print("Simple Calculator")
    while True:
        print("\n1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1-5): ")

        if choice in ('1', '2', '3', '4'):
            try:
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

            except ValueError as e:
                print(e)

        elif choice == '5':
            break

        else:
            print("Invalid choice. Please choose again.")

if __name__ == "__main__":
    calculator()
