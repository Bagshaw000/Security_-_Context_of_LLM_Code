

def add(x, y):
    
    return x + y


def subtract(x, y):
    
    return x - y


def multiply(x, y):
    
    return x * y


def divide(x, y):
    
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y


def main():
    print("Welcome to the Calculator Application!")
    
    while True:
        print("\nChoose an operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        
        choice = input("\nEnter your choice (1/2/3/4): ")
        
        if choice in ['1', '2', '3', '4']:
            num1 = float(input("Enter the first number: "))
            
            if choice == '1':
                num2 = float(input("Enter the second number: "))
                print(f"{num1} + {num2} = {add(num1, num2)}")
                
            elif choice == '2':
                num2 = float(input("Enter the second number: "))
                print(f"{num1} - {num2} = {subtract(num1, num2)}")
                
            elif choice == '3':
                num2 = float(input("Enter the second number: "))
                print(f"{num1} * {num2} = {multiply(num1, num2)}")
                
            elif choice == '4':
                try:
                    num2 = float(input("Enter the second number: "))
                    print(f"{num1} / {num2} = {divide(num1, num2)}")
                    
                except ZeroDivisionError as e:
                    print(e)
                    
        else:
            print("\nInvalid choice. Please choose again.")
            
        cont = input("\nDo you want to continue? (yes/no): ")
        
        if cont.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
