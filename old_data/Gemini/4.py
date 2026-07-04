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
            raise ValueError("Cannot divide by zero.")
        return a / b

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
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

def run_calculator_demo():
    calc = Calculator()
    
    try:
        val1 = 20
        val2 = 4
        
        print(f"Input values: {val1}, {val2}")
        print(f"Addition: {calc.add(val1, val2)}")
        print(f"Subtraction: {calc.subtract(val1, val2)}")
        print(f"Multiplication: {calc.multiply(val1, val2)}")
        print(f"Division: {calc.divide(val1, val2)}")
        
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    
    print("--- Calculator Demo ---")
    run_calculator_demo()
    
    
    print("\n--- Running Unit Tests ---")
    unittest.main(argv=['first-arg-is-ignored'], exit=False)