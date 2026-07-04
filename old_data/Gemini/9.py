import operator
import logging
import math
from typing import Dict, Callable, Union


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class CalculatorException(Exception):
    
    pass

class UnsupportedOperatorError(CalculatorException):
    
    pass

class MathematicalError(CalculatorException):
    
    pass

class Calculator:
    

    def __init__(self):
        
        self._operations: Dict[str, Callable[[float, float], float]] = {}
        self._initialize_defaults()

    def _initialize_defaults(self) -> None:
        
        self.register_operation("+", operator.add)
        self.register_operation("-", operator.sub)
        self.register_operation("*", operator.mul)
        self.register_operation("/", self._safe_divide)

    def _safe_divide(self, a: float, b: float) -> float:
        
        if b == 0:
            logger.error("DivisionByZero: Attempted to divide %s by zero", a)
            raise MathematicalError("Division by zero is mathematically undefined.")
        return a / b

    def register_operation(self, symbol: str, operation_func: Callable[[float, float], float]) -> None:
        
        if not callable(operation_func):
            raise CalculatorException("The operation handler must be a callable function.")
        
        self._operations[symbol] = operation_func
        logger.info("Operation '%s' registered successfully.", symbol)

    def calculate(self, operand_a: Union[int, float], operator_symbol: str, operand_b: Union[int, float]) -> float:
        
        if operator_symbol not in self._operations:
            logger.warning("Unsupported operator requested: %s", operator_symbol)
            raise UnsupportedOperatorError(f"Operator '{operator_symbol}' is not supported.")

        try:
            
            val_a = float(operand_a)
            val_b = float(operand_b)
            
            result = self._operations[operator_symbol](val_a, val_b)
            return result
        except ValueError as e:
            raise MathematicalError(f"Invalid operand type: {e}")
        except Exception as e:
            logger.exception("Unexpected error during calculation: %s", str(e))
            raise CalculatorException(f"An internal error occurred: {str(e)}")

def main():
    
    calc = Calculator()

    
    try:
        sum_val = calc.calculate(15, "+", 27)
        print(f"Addition Result: {sum_val}")

        
        calc.calculate(10, "/", 0)
    except CalculatorException as e:
        print(f"Handled Error: {e}")

    
    calc.register_operation("^", math.pow)
    pow_val = calc.calculate(2, "^", 10)
    print(f"Extended Operation (Power): 2 ^ 10 = {pow_val}")

    
    
    def custom_mod(a, b): return a % b
    calc.register_operation("mod", custom_mod)
    print(f"Custom Modulo: 10 mod 3 = {calc.calculate(10, 'mod', 3)}")

if __name__ == "__main__":
    main()