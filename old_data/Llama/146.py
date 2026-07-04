

def add(num1, num2):
    
    return num1 + num2

def subtract(num1, num2):
    
    return num1 - num2

def multiply(num1, num2):
    
    return num1 * num2

def divide(num1, num2):
    
    if num2 == 0:
        raise ValueError("Cannot divide by zero.")
    return num1 / num2

def calculator_menu():
    print("\nCalculator Menu:")
    while True:
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Quit")
        
        choice = input("Choose an operation (1-5): ")
        
        if choice in ['1', '2', '3', '4']:
            try:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))
                
                if choice == '1':
                    print(f"{num1} + {num2} = {add(num1, num2)}")
                elif choice == '2':
                    print(f"{num1} - {num2} = {subtract(num1, num2)}")
                elif choice == '3':
                    print(f"{num1} * {num2} = {multiply(num1, num2)}")
                elif choice == '4':
                    try:
                        result = divide(num1, num2)
                        print(f"{num1} / {num2} = {result}")
                    except ValueError as e:
                        print(e)
            except ValueError:
                print("Invalid input. Please enter a number.")
        else:
            print("Invalid choice. Quitting calculator.")
            break

if __name__ == "__main__":
    calculator_menu()
