from abc import ABC, abstractmethod
from typing import Dict, Type, Union
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Operation(ABC):
    
    @abstractmethod
    def execute(self, left_operand: float, right_operand: float) -> float:
        pass

class AddOperation(Operation):
    def execute(self, left_operand: float, right_operand: float) -> float:
        return left_operand + right_operand

class SubtractOperation(Operation):
    def execute(self, left_operand: float, right_operand: float) -> float:
        return left_operand - right_operand

class MultiplyOperation(Operation):
    def execute(self, left_operand: float, right_operand: float) -> float:
        return left_operand * right_operand

class DivideOperation(Operation):
    def execute(self, left_operand: float, right_operand: float) -> float:
        if right_operand == 0:
            raise ValueError("Mathematical Error: Division by zero is undefined.")
        return left_operand / right_operand

class Calculator:
    
    def __init__(self):
        self._operations: Dict[str, Operation] = {
            "+": AddOperation(),
            "-": SubtractOperation(),
            "*": MultiplyOperation(),
            "/": DivideOperation()
        }

    def register_operation(self, symbol: str, operation_strategy: Operation) -> None:
        
        self._operations[symbol] = operation_strategy

    def calculate(self, left_operand: Union[int, float], operator: str, right_operand: Union[int, float]) -> float:
        
        if operator not in self._operations:
            logger.error(f"Unsupported operation requested: {operator}")
            raise ValueError(f"Operator '{operator}' is not supported.")
        
        try:
            strategy = self._operations[operator]
            result = strategy.execute(float(left_operand), float(right_operand))
            return result
        except ValueError as e:
            logger.error(f"Calculation error: {e}")
            raise
        except Exception as e:
            logger.critical(f"Unexpected system error during calculation: {e}")
            raise

def main():
    
    calculator = Calculator()
    
    try:
        val1 = 15.5
        val2 = 5
        op = "/"
        
        result = calculator.calculate(val1, op, val2)
        print(f"Result of {val1} {op} {val2} = {result}")
        
    except ValueError as e:
        print(f"Client Error: {e}")
    except Exception as e:
        print(f"System Error: {e}")

if __name__ == "__main__":
    main()