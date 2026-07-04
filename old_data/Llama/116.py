
import operator

def calculator():
    
    print("Simple Calculator")
    print("-----------------")

    
    operators = {
        "+": operator.add,
        "-": operator.sub,
        "*": operator.mul,
        "/": operator.truediv
    }

    while True:
        
        num1 = float(input("Enter first number: "))

        
        op = input("Enter operation (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        
        if op not in operators:
            print("Invalid operator. Please try again.")
            continue

        
        result = operators[op](num1, num2)

        
        print(f"{num1} {op} {num2} = {result}")

        
        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != "y":
            break

if __name__ == "__main__":
    calculator()
