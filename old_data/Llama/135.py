
def add(x, y):
    return x + y

def subtract(x, y):
    return x - y

def multiply(x, y):
    return x * y

def divide(x, y):
    if y == 0:
        return "Error: Division by zero"
    else:
        return x / y

def main():
    print("Calculator Application")
    print("--------------------")

    while True:
        print("\nOptions:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Choose an option: ")

        if choice == "1":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = add(num1, num2)
            print(f"{num1} + {num2} = {result}")

        elif choice == "2":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = subtract(num1, num2)
            print(f"{num1} - {num2} = {result}")

        elif choice == "3":
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            result = multiply(num1, num2)
            print(f"{num1} * {num2} = {result}")

        elif choice == "4":
            num1 = float(input("Enter the dividend: "))
            num2 = float(input("Enter the divisor: "))
            result = divide(num1, num2)
            print(result)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid option. Please choose again.")

if __name__ == "__main__":
    main()
