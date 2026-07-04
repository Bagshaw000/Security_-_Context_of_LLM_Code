

import operator as op


operators = {
    '+': op.add,
    '-': op.sub,
    '*': op.mul,
    '/': op.truediv
}

def calculate(num1, num2, operator):
    
    if operator in operators:
        return operators[operator](num1, num2)
    else:
        raise ValueError("Invalid operator")

def main():
    print("Welcome to the Calculator!")

    while True:
        
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        if choice == "5":
            break

        elif choice in ["1", "2", "3", "4"]:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))

            print("\nChoose an operator:")
            print("1. Addition (+)")
            print("2. Subtraction (-)")
            print("3. Multiplication (*)")
            print("4. Division (/)")

            choice = input("Enter your choice (1-4): ")

            if choice in ["1", "2", "3", "4"]:
                operator = {
                    "1": "+",
                    "2": "-",
                    "3": "*",
                    "4": "/"
                }[choice]
                result = calculate(num1, num2, operator)
                print(f"\n{num1} {operator} {num2} = {result}")
            else:
                print("Invalid choice. Please try again.")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
