

class Calculator:
    def __init__(self):
        self.history = []

    def add(self, num1, num2):
        
        result = num1 + num2
        print(f"{num1} + {num2} = {result}")
        return result

    def subtract(self, num1, num2):
        
        result = num1 - num2
        print(f"{num1} - {num2} = {result}")
        return result

    def multiply(self, num1, num2):
        
        result = num1 * num2
        print(f"{num1} * {num2} = {result}")
        return result

    def divide(self, num1, num2):
        
        if num2 == 0:
            raise ValueError("Cannot divide by zero!")
        result = num1 / num2
        print(f"{num1} / {num2} = {result}")
        return result

    def calculate(self):
        
        while True:
            print("\nCalculator Menu:")
            print("1. Addition")
            print("2. Subtraction")
            print("3. Multiplication")
            print("4. Division")
            print("5. Quit")

            choice = input("Choose an operation (1-5): ")

            if choice in ["1", "2", "3", "4"]:
                num1 = float(input("Enter the first number: "))
                num2 = float(input("Enter the second number: "))

                if choice == "1":
                    result = self.add(num1, num2)
                elif choice == "2":
                    result = self.subtract(num1, num2)
                elif choice == "3":
                    result = self.multiply(num1, num2)
                else:
                    result = self.divide(num1, num2)

            elif choice == "5":
                print("\nGoodbye!")
                break

            else:
                print("Invalid choice. Please choose again.")

            cont = input("Do you want to continue? (y/n): ")

            if cont.lower() != 'y':
                break


if __name__ == "__main__":
    calc = Calculator()
    calc.calculate()
