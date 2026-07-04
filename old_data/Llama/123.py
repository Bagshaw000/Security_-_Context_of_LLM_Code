
class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        return num1 + num2

    def subtract(self, num1, num2):
        
        return num1 - num2

    def multiply(self, num1, num2):
        
        return num1 * num2

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero")
        return num1 / num2

    def calculate(self, operation, num1, num2):
        
        operations = {
            '+': self.add,
            '-': self.subtract,
            '*': self.multiply,
            '/': self.divide
        }
        if operation in operations:
            return operations[operation](num1, num2)
        else:
            raise ValueError("Invalid operation")

    def print_history(self):
        
        for i, (op, num1, num2) in enumerate(self.history):
            result = self.calculate(op, num1, num2)
            print(f"({num1}, {op}, {num2}) = {result}")


def main():
    calc = Calculator()
    
    while True:
        print("Operations:")
        print("+: Addition")
        print("-: Subtraction")
        print("*: Multiplication")
        print("/: Division")
        
        op = input("Choose an operation (+, -, *, /): ")
        
        try:
            num1 = float(input("Enter the first number: "))
            num2 = float(input("Enter the second number: "))
            
            result = calc.calculate(op, num1, num2)
            print(f"Result: {result}")
            
            calc.history.append((op, num1, num2))
        except ValueError as e:
            print(str(e))
        
        cont = input("Continue? (y/n): ")
        if cont.lower() != 'y':
            break


if __name__ == "__main__":
    main()
