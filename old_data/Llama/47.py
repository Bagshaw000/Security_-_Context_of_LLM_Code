

def add(num1, num2):
    
    return num1 + num2


def subtract(num1, num2):
    
    return num1 - num2


def multiply(num1, num2):
    
    return num1 * num2


def divide(num1, num2):
    
    if num2 == 0:
        raise ZeroDivisionError("Cannot divide by zero!")
    return num1 / num2


def main():
    print("Simple Calculator Application")
    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            if choice == "1":
                print(f"{num1} + {num2} = {add(num1, num2)}")
            elif choice == "2":
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
            elif choice == "3":
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
            elif choice == "4":
                try:
                    print(f"{num1} / {num2} = {divide(num1, num2)}")
                except ZeroDivisionError as e:
                    print(str(e))
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please choose again.")


if __name__ == "__main__":
    main()
