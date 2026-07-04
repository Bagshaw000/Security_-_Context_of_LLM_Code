import logging
from typing import Union, List, Optional


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("AmazonDeviceSystems-Calculator")

class CalculatorError(Exception):
    
    pass

class DivisionByZeroError(CalculatorError):
    
    pass

class ArithmeticService:
    

    def __init__(self):
        self._history: List[dict] = []

    def _record_transaction(self, operation: str, operands: List[float], result: float):
        
        entry = {
            "operation": operation,
            "operands": operands,
            "result": result
        }
        self._history.append(entry)
        logger.info(f"Executed {operation} on {operands} -> Result: {result}")

    def add(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a + b)
        self._record_transaction("ADDITION", [float(a), float(b)], result)
        return result

    def subtract(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a - b)
        self._record_transaction("SUBTRACTION", [float(a), float(b)], result)
        return result

    def multiply(self, a: Union[int, float], b: Union[int, float]) -> float:
        result = float(a * b)
        self._record_transaction("MULTIPLICATION", [float(a), float(b)], result)
        return result

    def divide(self, a: Union[int, float], b: Union[int, float]) -> float:
        if b == 0:
            logger.error("Validation failed: Division by zero attempted.")
            raise DivisionByZeroError("Denominator cannot be zero.")
        result = float(a / b)
        self._record_transaction("DIVISION", [float(a), float(b)], result)
        return result

    def get_execution_history(self) -> List[dict]:
        
        return self._history

def bootstrap_calculator():
    
    calc = ArithmeticService()
    
    try:
        
        val1 = calc.add(10.5, 4.5)
        val2 = calc.subtract(val1, 5)
        val3 = calc.multiply(val2, 2)
        val4 = calc.divide(val3, 4)
        
        print(f"Final Calculation Result: {val4}")
        
        
        print("\nAudit Log Summary:")
        for record in calc.get_execution_history():
            print(f"[{record['operation']}] Operands: {record['operands']} | Result: {record['result']}")

        
        

    except DivisionByZeroError as e:
        print(f"Business Logic Error: {e}")
    except Exception as e:
        print(f"Unexpected System Error: {e}")

if __name__ == "__main__":
    bootstrap_calculator()