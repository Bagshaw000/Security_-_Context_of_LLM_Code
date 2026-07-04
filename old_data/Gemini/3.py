import unittest

class Calculator:
    

    @staticmethod
    def add(a: float, b: float) -> float:
        return a + b

    @staticmethod
    def subtract(a: float, b: float) -> float:
        return a - b

    @staticmethod
    def multiply(a: float, b: float) -> float:
        return a * b

    @staticmethod
    def divide(a: float, b: float) -> float:
        if b == 0:
            raise ValueError("Division by zero is not permitted.")
        return a / b

class TestCalculator(unittest.TestCase):
    

    def test_addition(self):
        self.assertEqual(Calculator.add(5, 3), 8)
        self.assertEqual(Calculator.add(-1, 1), 0)

    def test_subtraction(self):
        self.assertEqual(Calculator.subtract(10, 4), 6)
        self.assertEqual(Calculator.subtract(0, 5), -5)

    def test_multiplication(self):
        self.assertEqual(Calculator.multiply(3, 3), 9)
        self.assertEqual(Calculator.multiply(-2, 4), -8)

    def test_division(self):
        self.assertEqual(Calculator.divide(10, 2), 5)
        with self.assertRaises(ValueError):
            Calculator.divide(10, 0)

def main():
    
    print("Bristol Inventory Tools - Calculator Module")
    print("-------------------------------------------")
    
    try:
        val1 = float(input("Enter first operand: "))
        val2 = float(input("Enter second operand: "))
        operation = input("Select operation (+, -, *, /): ").strip()

        if operation == '+':
            print(f"Result: {Calculator.add(val1, val2)}")
        elif operation == '-':
            print(f"Result: {Calculator.subtract(val1, val2)}")
        elif operation == '*':
            print(f"Result: {Calculator.multiply(val1, val2)}")
        elif operation == '/':
            print(f"Result: {Calculator.divide(val1, val2)}")
        else:
            print("Error: Invalid operation selected.")
            
    except ValueError as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestCalculator)
    test_result = unittest.TextTestRunner(verbosity=0).run(suite)
    
    if test_result.wasSuccessful():
        main()
    else:
        print("Build Failure: Unit tests failed. Aborting application launch.")