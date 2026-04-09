import numpy as np
from typing import Callable, Tuple, Optional

class GlobalGradientAscent:
    

    def __init__(
        self, 
        learning_rate: float = 0.01, 
        max_iterations: int = 1000, 
        precision: float = 1e-8,
        num_restarts: int = 20
    ):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.precision = precision
        self.num_restarts = num_restarts

    def find_global_maximum(
        self, 
        objective: Callable[[np.ndarray], float], 
        gradient: Callable[[np.ndarray], np.ndarray], 
        bounds: Tuple[np.ndarray, np.ndarray]
    ) -> Tuple[np.ndarray, float]:
        
        lower_bound, upper_bound = bounds
        best_x = None
        best_value = -np.inf

        for _ in range(self.num_restarts):
            
            current_x = np.random.uniform(lower_bound, upper_bound)
            
            for i in range(self.max_iterations):
                grad_val = gradient(current_x)
                
                
                next_x = current_x + self.learning_rate * grad_val
                
                
                next_x = np.clip(next_x, lower_bound, upper_bound)
                
                
                if np.linalg.norm(next_x - current_x) < self.precision:
                    break
                
                current_x = next_x
            
            
            current_value = objective(current_x)
            if current_value > best_value:
                best_value = current_value
                best_x = current_x

        return best_x, best_value

def example_objective(x: np.ndarray) -> float:
    
    
    return -(x[0]**2) + 10 * np.cos(x[0])

def example_gradient(x: np.ndarray) -> np.ndarray:
    
    return np.array([-2 * x[0] - 10 * np.sin(x[0])])

if __name__ == "__main__":
    
    optimizer = GlobalGradientAscent(
        learning_rate=0.05, 
        max_iterations=500, 
        num_restarts=50
    )
    
    
    search_bounds = (np.array([-10.0]), np.array([10.0]))
    
    peak_coords, peak_val = optimizer.find_global_maximum(
        example_objective, 
        example_gradient, 
        search_bounds
    )
    
    print(f"Optimization Complete.")
    print(f"Global Maximum Coordinates: {peak_coords}")
    print(f"Maximum Function Value: {peak_val}")