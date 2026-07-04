
def add(num1, num2):
    
    return num1 + num2

def subtract(num1, num2):
    
    return num1 - num2

def multiply(num1, num2):
    
    return num1 * num2

def divide(num1, num2):
    
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2

def main():
    print("Calculator Application")
    print("---------------------")

    while True:
        print("\nOperations:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your operation (1-5): ")

        if choice == "5":
            break

        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

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

        else:
            print("Invalid operation. Please choose a valid option.")

if __name__ == "__main__":
    main()
