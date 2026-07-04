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
            raise ValueError("Division by zero is not permitted.")
        return x / y

class TestCalculator(unittest.TestCase):
    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(10, 5), 15)
        self.assertEqual(self.calc.add(-1, 1), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 5), 5)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 7), 21)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

def main():
    calc = Calculator()
    
    print("--- Junior Engineer Calculator Module ---")
    try:
        a = 15
        b = 3
        print(f"Addition: {a} + {b} = {calc.add(a, b)}")
        print(f"Subtraction: {a} - {b} = {calc.subtract(a, b)}")
        print(f"Multiplication: {a} * {b} = {calc.multiply(a, b)}")
        print(f"Division: {a} / {b} = {calc.divide(a, b)}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    main()
    
    
    print("\nRunning Unit Tests...")
    unittest.main(argv=[''], exit=False)