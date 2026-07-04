import operator

def calculator():
    print("Calculator Application")
    print("---------------------")

    
    operations = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    while True:
        print("\nMenu:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Exit")

        choice = input("Enter your choice (1-5): ")

        if choice in operations:
            num1 = float(input("Enter first number: "))
            num2 = float(input("Enter second number: "))

            result = operations[choice](num1, num2)

            print(f"{num1} {choice} {num2} = {result}")
        elif choice == '5':
            print("Exiting the calculator application")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    calculator()