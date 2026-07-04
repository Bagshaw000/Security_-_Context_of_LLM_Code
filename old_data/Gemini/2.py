import unittest

class Calculator:
    

    def add(self, x: float, y: float) -> float:
        return x + y

    def subtract(self, x: float, y: float) -> float:
        return x - y

    def multiply(self, x: float, y: float) -> float:
        return x * y

    def divide(self, x: float, y: float) -> float:
        if y == 0:
            raise ValueError("Division by zero is not allowed.")
        return x / y


class TestCalculator(unittest.TestCase):
    

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)
        self.assertEqual(self.calc.subtract(0, 5), -5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 7), 21)
        self.assertEqual(self.calc.multiply(-2, 4), -8)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        self.assertEqual(self.calc.divide(5, 2), 2.5)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)


def run_calculator():
    calc = Calculator()
    print("--- John's Python Calculator ---")
    
    try:
        num1 = float(input("Enter first number: "))
        op = input("Enter operator (+, -, *, /): ")
        num2 = float(input("Enter second number: "))

        if op == '+':
            print(f"Result: {calc.add(num1, num2)}")
        elif op == '-':
            print(f"Result: {calc.subtract(num1, num2)}")
        elif op == '*':
            print(f"Result: {calc.multiply(num1, num2)}")
        elif op == '/':
            print(f"Result: {calc.divide(num1, num2)}")
        else:
            print("Invalid operator.")
    except ValueError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    
    
    print("Running unit tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    unittest.TextTestRunner(verbosity=1).run(suite)
    
    print("\nStarting Calculator Application...")
    run_calculator()