import numpy as np
from typing import Callable, Tuple, Optional

class GlobalGradientAscent:
    

    def __init__(
        self, 
        learning_rate: float = 0.01, 
        max_iterations: int = 1000, 
        convergence_threshold: float = 1e-8,
        num_restarts: int = 50
    ):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.convergence_threshold = convergence_threshold
        self.num_restarts = num_restarts

    def find_global_maximum(
        self, 
        objective_fn: Callable[[np.ndarray], float], 
        gradient_fn: Callable[[np.ndarray], np.ndarray], 
        lower_bound: np.ndarray, 
        upper_bound: np.ndarray
    ) -> Tuple[Optional[np.ndarray], float]:
        
        best_params = None
        global_max_value = -np.inf

        for _ in range(self.num_restarts):
            
            current_params = np.random.uniform(lower_bound, upper_bound)
            
            for i in range(self.max_iterations):
                gradient = gradient_fn(current_params)
                
                
                update_step = self.learning_rate * gradient
                
                
                if np.linalg.norm(update_step) < self.convergence_threshold:
                    break
                
                
                next_params = current_params + update_step
                
                
                current_params = np.clip(next_params, lower_bound, upper_bound)

            
            current_value = objective_fn(current_params)
            
            
            if current_value > global_max_value:
                global_max_value = current_value
                best_params = np.copy(current_params)

        return best_params, global_max_value

def example_usage():
    
    
    def objective(x: np.ndarray) -> float:
        return float(np.sin(x[0]) - 0.1 * (x[0]**2))

    def gradient(x: np.ndarray) -> np.ndarray:
        return np.array([np.cos(x[0]) - 0.2 * x[0]])

    
    lb = np.array([-10.0])
    ub = np.array([10.0])

    
    optimizer = GlobalGradientAscent(
        learning_rate=0.1, 
        num_restarts=20
    )

    
    best_x, max_val = optimizer.find_global_maximum(objective, gradient, lb, ub)
    return best_x, max_val

if __name__ == "__main__":
    x_star, y_star = example_usage()
    print(f"Optimal Parameters: {x_star}")
    print(f"Global Maximum Value: {y_star}")