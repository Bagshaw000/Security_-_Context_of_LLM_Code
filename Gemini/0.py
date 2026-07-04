import unittest
import sys

class Calculator:
    

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ValueError("Error: Division by zero is undefined.")
        return a / b

def display_menu():
    print("\n--- Junior Engineer Calculator CLI ---")
    print("Available operations: add, subtract, multiply, divide")
    print("Type 'exit' to close the program.")
    print("Type 'test' to run unit tests.")

def main():
    calc = Calculator()
    
    while True:
        display_menu()
        choice = input("Select operation or command: ").strip().lower()

        if choice == 'exit':
            print("Shutting down...")
            break
        
        if choice == 'test':
            print("Running suite of unit tests...")
            
            suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
            unittest.TextTestRunner(verbosity=2).run(suite)
            continue

        if choice in ['add', 'subtract', 'multiply', 'divide']:
            try:
                x = float(input("Enter first number: "))
                y = float(input("Enter second number: "))

                if choice == 'add':
                    print(f"Result: {calc.add(x, y)}")
                elif choice == 'subtract':
                    print(f"Result: {calc.subtract(x, y)}")
                elif choice == 'multiply':
                    print(f"Result: {calc.multiply(x, y)}")
                elif choice == 'divide':
                    print(f"Result: {calc.divide(x, y)}")
            except ValueError as e:
                print(f"Input Error: {e}")
        else:
            print("Invalid selection. Please try again.")

class TestCalculator(unittest.TestCase):
    

    def setUp(self):
        self.calc = Calculator()

    def test_addition(self):
        self.assertEqual(self.calc.add(5, 5), 10)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtraction(self):
        self.assertEqual(self.calc.subtract(20, 5), 15)

    def test_multiplication(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(10, 0), 0)

    def test_division(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

if __name__ == "__main__":
    
    if len(sys.argv) > 1 and sys.argv[1] == 'run-tests':
        unittest.main(argv=[sys.argv[0]])
    else:
        main()