
def add(num1, num2):
    
    return num1 + num2

def subtract(num1, num2):
    
    return num1 - num2

def multiply(num1, num2):
    
    return num1 * num2

def divide(num1, num2):
    
    if num2 == 0:
        raise ValueError("Cannot divide by zero!")
    return num1 / num2

def calculator():
    print("Calculator Application")
    print("-----------------------")

    while True:
        try:
            num1 = float(input("Enter first number: "))
            operator = input("Enter operation (+, -, *, /): ")
            num2 = float(input("Enter second number: "))

            if operator == "+":
                result = add(num1, num2)
                print(f"{num1} + {num2} = {result}")
            elif operator == "-":
                result = subtract(num1, num2)
                print(f"{num1} - {num2} = {result}")
            elif operator == "*":
                result = multiply(num1, num2)
                print(f"{num1} * {num2} = {result}")
            elif operator == "/":
                try:
                    result = divide(num1, num2)
                    print(f"{num1} / {num2} = {result}")
                except ValueError as e:
                    print(e)
            else:
                print("Invalid operator. Please enter one of the following: +, -, *, /")
        except ValueError as e:
            print(e)

        again = input("Do you want to perform another operation? (yes/no): ")
        if again.lower() != "yes":
            break

if __name__ == "__main__":
    calculator()
