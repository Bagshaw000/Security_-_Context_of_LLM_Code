
import operator

def calculator():
    
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    print("Calculator Application")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")

    while True:
        choice = input("Enter your choice (1/2/3/4): ")

        
        if choice == '4':
            break

        
        if choice not in ['1', '2', '3', '4']:
            print("Invalid choice. Please choose again.")
            continue

        
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        
        if choice == '1':
            print(f"{num1} + {num2} = {ops[choice](num1, num2)}")
        elif choice == '2':
            print(f"{num1} - {num2} = {ops[choice](num1, num2)}")
        elif choice == '3':
            print(f"{num1} * {num2} = {ops[choice](num1, num2)}")
        elif choice == '4':
            if num2 != 0:
                print(f"{num1} / {num2} = {ops[choice](num1, num2)}")
            else:
                print("Error! Division by zero is not allowed.")


calculator()
