import math
import logging
from typing import Dict, Callable, Union


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("DeviceMgmtCalculator")

class CalculatorError(Exception):
    
    pass

class ArithmeticError(CalculatorError):
    
    pass

class InvalidOperationError(CalculatorError):
    
    pass

class Calculator:
    

    def __init__(self):
        
        self._operations: Dict[str, Callable[[float, float], float]] = {
            "+": self._add,
            "-": self._subtract,
            "*": self._multiply,
            "/": self._divide,
            "^": self._power
        }
        logger.info("Calculator service initialized with core arithmetic registry.")

    def _add(self, a: float, b: float) -> float:
        return a + b

    def _subtract(self, a: float, b: float) -> float:
        return a - b

    def _multiply(self, a: float, b: float) -> float:
        return a * b

    def _divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ArithmeticError("Division by zero is undefined in this domain.")
        return a / b

    def _power(self, a: float, b: float) -> float:
        return math.pow(a, b)

    def register_operation(self, symbol: str, func: Callable[[float, float], float]) -> None:
        
        self._operations[symbol] = func
        logger.info(f"Registered new operation: {symbol}")

    def evaluate(self, op: str, a: Union[int, float], b: Union[int, float]) -> float:
        
        operation_func = self._operations.get(op)
        
        if not operation_func:
            logger.error(f"Unsupported operation call: {op}")
            raise InvalidOperationError(f"Operation '{op}' is not supported by the current engine.")

        try:
            
            result = operation_func(float(a), float(b))
            logger.debug(f"Operation successful: {a} {op} {b} = {result}")
            return result
        except ArithmeticError:
            raise
        except Exception as e:
            logger.exception("Unexpected system failure during evaluation.")
            raise CalculatorError("Internal processing error.") from e

def main():
    
    calc = Calculator()

    
    try:
        print(f"Addition: {calc.evaluate('+', 15, 27)}")
        print(f"Division: {calc.evaluate('/', 100, 5)}")
        print(f"Exponent: {calc.evaluate('^', 2, 10)}")
        
        
        calc.evaluate('/', 10, 0)
    except CalculatorError as e:
        print(f"Caught expected error: {e}")

    
    calc.register_operation("%", lambda a, b: a % b)
    print(f"Modulo: {calc.evaluate('%', 10, 3)}")

if __name__ == "__main__":
    main()