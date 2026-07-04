
import operator


operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def display_menu():
    
    print("Calculator Menu:")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Quit")

def perform_operation():
    
    num1 = float(input("Enter the first number: "))
    operator_symbol = input("Enter the operator (+, -, *, /): ")
    num2 = float(input("Enter the second number: "))

    if operator_symbol in operators:
        result = operators[operator_symbol](num1, num2)
        print(f"{num1} {operator_symbol} {num2} = {result}")
    else:
        print("Invalid operator")

def main():
    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ")
        
        if choice in ['1', '2', '3', '4']:
            perform_operation()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()
