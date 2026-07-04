class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        result = num1 + num2
        self.history.append(f"Added {num1} and {num2}, Result: {result}")
        return result

    def subtract(self, num1, num2):
        result = num1 - num2
        self.history.append(f"Subtracted {num2} from {num1}, Result: {result}")
        return result

    def multiply(self, num1, num2):
        result = num1 * num2
        self.history.append(f"Multiply {num1} and {num2}, Result: {result}")
        return result

    def divide(self, num1, num2):
        if num2 == 0:
            return "Error! Division by zero is not allowed"
        else:
            result = num1 / num2
            self.history.append(f"Divided {num1} by {num2}, Result: {result}")
            return result

    def display_history(self):
        for entry in self.history:
            print(entry)

def main():
    calculator = Calculator()
    while True:
        print("Select operation:")
        print("1. Addition")
        print("2. Subtraction")
        print("3. Multiplication")
        print("4. Division")
        print("5. Display History")
        print("6. Exit")
        
        choice = input("Enter your choice(1/2/3/4/5/6): ")
        
        if choice in ('1', '2', '3', '4'):
            try:
                num1 = float(input("Enter first number: "))
                num2 = float(input("Enter second number: "))
                
                if choice == '1':
                    print(calculator.add(num1, num2))
                elif choice == '2':
                    print(calculator.subtract(num1, num2))
                elif choice == '3':
                    print(calculator.multiply(num1, num2))
                elif choice == '4':
                    print(calculator.divide(num1, num2))
                    
            except ValueError:
                print("Invalid input. Please enter a number.")
        
        elif choice == '5':
            calculator.display_history()
            
        elif choice == '6':
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()