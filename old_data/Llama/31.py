

import operator

def calculator():
    
    ops = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    
    num1 = float(input("Enter the first number: "))
    op = input("Enter the operator (+, -, *, /): ")
    num2 = float(input("Enter the second number: "))

    
    if op not in ops:
        print("Invalid operator. Please try again.")
        return calculator()

    
    result = ops[op](num1, num2)

    
    print(f"{num1} {op} {num2} = {result}")


if __name__ == "__main__":
    calculator()
