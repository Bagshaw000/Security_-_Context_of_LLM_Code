import math
import logging
import threading
from abc import ABC, abstractmethod
from typing import List, Optional, Final, Tuple
from dataclasses import dataclass


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("SecureOptimizer")

class OptimizationError(Exception):
    
    pass

class InputValidationError(OptimizationError):
    
    pass

class NumericalStabilityError(OptimizationError):
    
    pass

@dataclass(frozen=True)
class OptimizerConfig:
    
    learning_rate: float = 0.01
    max_iterations: int = 1000
    tolerance: float = 1e-6
    max_value_threshold: float = 1e15  
    min_learning_rate: float = 1e-12

class ObjectiveFunction(ABC):
    
    @abstractmethod
    def compute_value(self, point: List[float]) -> float:
        
        pass

    @abstractmethod
    def compute_gradient(self, point: List[float]) -> List[float]:
        
        pass

class GradientAscentOptimizer:
    

    def __init__(self, config: OptimizerConfig = OptimizerConfig()):
        self._config = config
        self._lock = threading.RLock()
        self._validate_config(config)

    def _validate_config(self, config: OptimizerConfig) -> None:
        
        if not (0 < config.learning_rate < 1):
            raise InputValidationError("Learning rate must be in range (0, 1).")
        if config.max_iterations <= 0:
            raise InputValidationError("Max iterations must be positive.")
        if not math.isfinite(config.max_value_threshold):
            raise InputValidationError("Value threshold must be a finite number.")

    def _sanitize_point(self, point: List[float]) -> None:
        
        if not point:
            raise InputValidationError("Input point cannot be empty.")
        for val in point:
            if not math.isfinite(val):
                raise InputValidationError("Point components must be finite real numbers.")
            if abs(val) > self._config.max_value_threshold:
                raise InputValidationError("Input exceeds safety bounds.")

    def _check_numerical_stability(self, values: List[float]) -> None:
        
        for v in values:
            if not math.isfinite(v):
                raise NumericalStabilityError("Non-finite value detected during optimization.")

    def optimize(self, objective: ObjectiveFunction, initial_point: List[float]) -> Tuple[List[float], float]:
        
        with self._lock:
            self._sanitize_point(initial_point)
            
            current_point = list(initial_point)
            iteration = 0
            
            logger.info(f"Starting optimization. Max iterations: {self._config.max_iterations}")

            while iteration < self._config.max_iterations:
                try:
                    gradient = objective.compute_gradient(current_point)
                    self._check_numerical_stability(gradient)

                    
                    new_point = []
                    gradient_norm_sq = 0.0
                    
                    for i in range(len(current_point)):
                        delta = self._config.learning_rate * gradient[i]
                        updated_val = current_point[i] + delta
                        
                        
                        if abs(updated_val) > self._config.max_value_threshold:
                            logger.warning("Saturation point reached. Clipping value.")
                            updated_val = math.copysign(self._config.max_value_threshold, updated_val)
                        
                        new_point.append(updated_val)
                        gradient_norm_sq += gradient[i] ** 2

                    
                    if math.sqrt(gradient_norm_sq) < self._config.tolerance:
                        logger.info(f"Convergence reached at iteration {iteration}.")
                        break

                    current_point = new_point
                    iteration += 1

                except Exception as e:
                    logger.error(f"Critical failure during optimization loop: {str(e)}")
                    raise OptimizationError("Internal optimization failure.") from e

            final_value = objective.compute_value(current_point)
            self._check_numerical_stability([final_value])
            
            logger.info("Optimization cycle completed successfully.")
            return current_point, final_value

class SecureObjective(ObjectiveFunction):
    
    def compute_value(self, point: List[float]) -> float:
        
        return -((point[0] - 5) ** 2) + 10

    def compute_gradient(self, point: List[float]) -> List[float]:
        
        return [-2 * (point[0] - 5)]

def main():
    
    try:
        config = OptimizerConfig(learning_rate=0.1, max_iterations=500)
        optimizer = GradientAscentOptimizer(config)
        objective = SecureObjective()
        
        
        start_point = [0.0]
        
        
        optimal_point, max_val = optimizer.optimize(objective, start_point)
        
        print(f"Optimal Point: {optimal_point}")
        print(f"Maximum Value: {max_val}")
        
    except OptimizationError as oe:
        print(f"System Error: {oe}")
    except Exception as e:
        print(f"Unexpected System Fault: {e}")

if __name__ == "__main__":
    main()