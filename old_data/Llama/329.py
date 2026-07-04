
import operator


operators = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv
}

def calculate(num1, num2, operator):
    if operator in operators:
        return operators[operator](num1, num2)
    else:
        print("Invalid operator. Please use one of the following: +, -, *, /")
        return None

def main():
    while True:
        
        num1 = float(input("Enter first number: "))

        
        num2 = float(input("Enter second number: "))

        
        print("\nAvailable operators:")
        for op in operators:
            print(op)

        
        operator = input("\nEnter an operator (+, -, *, /): ")

        
        result = calculate(num1, num2, operator)
        if result is not None:
            print(f"\nResult: {result}")

        
        choice = input("\nDo you want to perform another calculation? (yes/no): ")
        if choice.lower() != "yes":
            break

if __name__ == "__main__":
    main()
