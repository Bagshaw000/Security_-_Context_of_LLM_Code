

import operator

def calculator():
    

    
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    
    num1 = float(input("Enter the first number: "))
    op = input("Enter the operator (+, -, *, /): ")
    num2 = float(input("Enter the second number: "))

    
    if op not in operators:
        print("Invalid operator. Please use +, -, *, or /.")
        return None

    
    try:
        result = operators[op](num1, num2)
        print(f"{num1} {op} {num2} = {result}")
    except ZeroDivisionError:
        print("Cannot divide by zero!")
        return None


while True:
    calculator()
    
    
    cont = input("Do you want to perform another calculation? (y/n): ")
    if cont.lower() != 'y':
        break

