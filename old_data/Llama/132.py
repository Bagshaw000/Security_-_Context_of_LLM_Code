
import operator

def calculator():
    print("Simple Calculator")
    print("-----------------")

    
    operators = {
        '+': operator.add,
        '-': operator.sub,
        '*': operator.mul,
        '/': operator.truediv
    }

    while True:
        num1 = float(input("Enter first number: "))
        operation = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if operation in operators:
            try:
                result = operators[operation](num1, num2)
                print(f"{num1} {operation} {num2} = {result}")
            except ZeroDivisionError:
                print("Cannot divide by zero!")
        else:
            print("Invalid operation!")

        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != 'y':
            break

if __name__ == "__main__":
    calculator()
