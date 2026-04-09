import math
import logging
from typing import Callable, Dict, Union


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CalculatorError(Exception):
    
    pass

class DivisionByZeroError(CalculatorError):
    
    pass

class ArithmeticOperation:
    
    def execute(self, a: float, b: float) -> float:
        raise NotImplementedError

class Addition(ArithmeticOperation):
    def execute(self, a: float, b: float) -> float:
        return a + b

class Subtraction(ArithmeticOperation):
    def execute(self, a: float, b: float) -> float:
        return a - b

class Multiplication(ArithmeticOperation):
    def execute(self, a: float, b: float) -> float:
        return a * b

class Division(ArithmeticOperation):
    def execute(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("Illegal operation: Division by zero.")
        return a / b

class CalculatorEngine:
    
    def __init__(self):
        self._operations: Dict[str, ArithmeticOperation] = {
            "+": Addition(),
            "-": Subtraction(),
            "*": Multiplication(),
            "/": Division()
        }

    def register_operation(self, symbol: str, operation: ArithmeticOperation):
        
        self._operations[symbol] = operation

    def calculate(self, operand_a: float, operator: str, operand_b: float) -> float:
        if operator not in self._operations:
            raise CalculatorError(f"Operator '{operator}' is not supported.")
        
        operation = self._operations[operator]
        return operation.execute(operand_a, operand_b)

class CalculatorApp:
    
    def __init__(self):
        self.engine = CalculatorEngine()

    def start(self):
        print("--- Amazon Device Management Systems: Internal Math Utility ---")
        print("Supported operations: +, -, *, /")
        print("Enter 'quit' to exit.")

        while True:
            try:
                user_input = input("\nEnter expression (e.g., 10 + 5): ").strip()
                
                if user_input.lower() == 'quit':
                    logging.info("Shutting down calculator service.")
                    break

                
                parts = user_input.split()
                if len(parts) != 3:
                    print("Invalid syntax. Please use format: [number] [operator] [number]")
                    continue

                a = float(parts[0])
                op = parts[1]
                b = float(parts[2])

                result = self.engine.calculate(a, op, b)
                print(f"Result: {result}")

            except ValueError:
                print("Input Error: Operands must be valid numbers.")
            except CalculatorError as e:
                print(f"Business Logic Error: {e}")
            except Exception as e:
                logging.error(f"Unexpected system error: {e}")

if __name__ == "__main__":
    
    app = CalculatorApp()
    app.start()