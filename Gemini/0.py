import unittest

class Calculator:
    
    def add(self, a: float, b: float) -> float:
        return a + b

    def subtract(self, a: float, b: float) -> float:
        return a - b

    def multiply(self, a: float, b: float) -> float:
        return a * b

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is undefined.")
        return a / b

class TestCalculator(unittest.TestCase):
    
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10.5, 4.5), 15.0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 7), 21)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

def main():
    calc = Calculator()
    print("--- Junior Engineer Calculator Utility ---")
    
    try:
        val1 = float(input("Enter first operand: "))
        operation = input("Enter operation (+, -, *, /): ").strip()
        val2 = float(input("Enter second operand: "))

        if operation == '+':
            result = calc.add(val1, val2)
        elif operation == '-':
            result = calc.subtract(val1, val2)
        elif operation == '*':
            result = calc.multiply(val1, val2)
        elif operation == '/':
            result = calc.divide(val1, val2)
        else:
            print("Unsupported operation.")
            return

        print(f"Output: {result}")

    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected system error occurred: {e}")

if __name__ == "__main__":
    
    print("Executing internal unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    result = unittest.TextTestRunner(verbosity=0).run(suite)
    
    if result.wasSuccessful():
        print("Tests passed. Launching application...\n")
        main()
    else:
        print("Tests failed. Aborting launch.")