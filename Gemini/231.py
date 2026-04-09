import numpy as np
from typing import Callable, Tuple, List

class GradientAscentOptimizer:
    

    def __init__(self, learning_rate: float = 0.01, tolerance: float = 1e-7, max_iterations: int = 1000):
        
        self.learning_rate = learning_rate
        self.tolerance = tolerance
        self.max_iterations = max_iterations

    def find_global_maximum(
        self, 
        objective_function: Callable[[np.ndarray], float], 
        gradient_function: Callable[[np.ndarray], np.ndarray], 
        bounds: List[Tuple[float, float]], 
        num_restarts: int = 25
    ) -> Tuple[np.ndarray, float]:
        
        best_x = None
        best_value = -np.inf
        
        bounds_arr = np.array(bounds)
        dimensions = len(bounds)

        for attempt in range(num_restarts):
            
            initial_x = np.random.uniform(bounds_arr[:, 0], bounds_arr[:, 1], size=dimensions)
            
            
            candidate_x, candidate_value = self._perform_ascent(
                objective_function, 
                gradient_function, 
                initial_x, 
                bounds_arr
            )
            
            
            if candidate_value > best_value:
                best_value = candidate_value
                best_x = candidate_x
                
        return best_x, best_value

    def _perform_ascent(
        self, 
        f: Callable[[np.ndarray], float], 
        grad_f: Callable[[np.ndarray], np.ndarray], 
        start_x: np.ndarray,
        bounds: np.ndarray
    ) -> Tuple[np.ndarray, float]:
        
        current_x = start_x.copy()
        
        for _ in range(self.max_iterations):
            gradient = grad_f(current_x)
            
            
            if np.linalg.norm(gradient) < self.tolerance:
                break
            
            
            next_x = current_x + self.learning_rate * gradient
            
            
            next_x = np.clip(next_x, bounds[:, 0], bounds[:, 1])
            
            
            if np.linalg.norm(next_x - current_x) < self.tolerance:
                break
                
            current_x = next_x
            
        return current_x, f(current_x)

def example_complex_objective(x: np.ndarray) -> float:
    
    return -(x[0]**2) + np.sin(5 * x[0])

def example_complex_gradient(x: np.ndarray) -> np.ndarray:
    
    return np.array([-2 * x[0] + 5 * np.cos(5 * x[0])])

if __name__ == "__main__":
    
    optimizer = GradientAscentOptimizer(
        learning_rate=0.01, 
        max_iterations=5000, 
        tolerance=1e-8
    )
    
    
    search_space = [(-5.0, 5.0)]
    
    
    global_max_coords, global_max_val = optimizer.find_global_maximum(
        example_complex_objective, 
        example_complex_gradient, 
        search_space, 
        num_restarts=50
    )
    
    print(f"Optimization Complete.")
    print(f"Global Maximum Coordinates: {global_max_coords}")
    print(f"Global Maximum Value: {global_max_val}")