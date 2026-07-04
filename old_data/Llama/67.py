
import operator


operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def calculator():
    
    while True:
        print("Simple Calculator Menu")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")

        choice = input("Enter your choice (1-5): ")

        
        if choice == '5':
            break

        
        num1 = float(input("Enter first number: "))
        operator_char = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        
        try:
            result = operators[operator_char](num1, num2)
            print(f"{num1} {operator_char} {num2} = {result}")
        except ZeroDivisionError:
            print("Error! Division by zero is not allowed.")
        except KeyError:
            print("Error! Invalid operator. Please use +, -, *, /.")


calculator()
