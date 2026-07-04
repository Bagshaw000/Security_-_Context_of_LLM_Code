from typing import Union, List, Optional
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("AmazonDeviceManagement.Calculator")

class CalculatorError(Exception):
    
    pass

class DivisionByZeroError(CalculatorError):
    
    pass

class Calculator:
    

    def __init__(self) -> None:
        self._history: List[str] = []

    def _log_operation(self, operation: str, result: float) -> None:
        entry = f"Operation: {operation}, Result: {result}"
        self._history.append(entry)
        logger.info(entry)

    def add(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a + b)
        self._log_operation(f"{a} + {b}", result)
        return result

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a - b)
        self._log_operation(f"{a} - {b}", result)
        return result

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a * b)
        self._log_operation(f"{a} * {b}", result)
        return result

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        if b == 0:
            logger.error("Attempted division by zero.")
            raise DivisionByZeroError("The divisor cannot be zero.")
        result = float(a / b)
        self._log_operation(f"{a} / {b}", result)
        return result

    def get_last_operation(self) -> Optional[str]:
        return self._history[-1] if self._history else None

def run_service_simulation():
    
    calc = Calculator()

    try:
        
        sum_val = calc.add(10, 5)
        diff_val = calc.subtract(20, 4.5)
        prod_val = calc.multiply(3, 7)
        div_val = calc.divide(100, 4)

        print(f"Sum: {sum_val}")
        print(f"Difference: {diff_val}")
        print(f"Product: {prod_val}")
        print(f"Quotient: {div_val}")

        
        calc.divide(10, 0)

    except DivisionByZeroError as e:
        print(f"Handled expected error: {e}")
    except Exception as e:
        print(f"Unexpected system error: {e}")

if __name__ == "__main__":
    run_service_simulation()