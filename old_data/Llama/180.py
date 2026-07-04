

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
    print("Calculator Application")
    print("---------------------")

    while True:
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an operation (1/2/3/4/5): ")

        if choice == "5":
            break

        elif choice not in ["1", "2", "3", "4"]:
            print("Invalid choice! Please choose again.")
            continue

        num1 = float(input("Enter the first number: "))
        num2 = float(input("Enter the second number: "))

        if choice == "1":
            result = add(num1, num2)
            print(f"{num1} + {num2} = {result}")

        elif choice == "2":
            result = subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")

        elif choice == "3":
            result = multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")

        elif choice == "4":
            try:
                result = divide(num1, num2)
                print(f"{num1} / {num2} = {result}")
            except ValueError as e:
                print(e)

if __name__ == "__main__":
    calculator()
