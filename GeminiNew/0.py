import sys
import unittest

class SecureCalculator:
    
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
            raise ValueError("Mathematical Error: Division by zero is not allowed.")
        return a / b

def validate_and_parse(user_input: str):
    
    parts = user_input.strip().split()
    
    if len(parts) != 3:
        raise ValueError("Format Error: Input must be 'number operator number' (e.g., 5 + 5).")
    
    try:
        num1 = float(parts[0])
        num2 = float(parts[2])
    except ValueError:
        raise ValueError("Type Error: Operands must