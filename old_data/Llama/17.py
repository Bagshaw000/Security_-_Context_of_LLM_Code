
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
            raise ValueError("Cannot divide by zero.")
        return num1 / num2

    def calculate(self, op, num1, num2):
        
        try:
            if op == "+":
                result = self.add(num1, num2)
            elif op == "-":
                result = self.subtract(num1, num2)
            elif op == "*":
                result = self.multiply(num1, num2)
            elif op == "/":
                result = self.divide(num1, num2)
            else:
                raise ValueError("Invalid operation.")
            self.history.append((op, num1, num2, result))
            return result
        except ValueError as e:
            print(e)

    def display_history(self):
        
        for i, (op, num1, num2, result) in enumerate(self.history, start=1):
            print(f"Calculation {i}: {op} {num1} {op} {num2} = {result}")


def main():
    calc = Calculator()
    while True:
        op = input("Enter operation (+, -, *, /): ")
        num1 = float(input("Enter first number: "))
        num2 = float(input("Enter second number: "))

        try:
            result = calc.calculate(op, num1, num2)
            print(f"Result: {result}")
        except ValueError as e:
            print(e)

        cont = input("Do you want to continue? (y/n): ")
        if cont.lower() != 'y':
            break

    calc.display_history()


if __name__ == "__main__":
    main()
