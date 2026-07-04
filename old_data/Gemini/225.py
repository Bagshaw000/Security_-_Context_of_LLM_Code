import random
import math
from typing import Callable, Tuple

def gradient_ascent(
    grad_func: Callable[[float], float],
    start_x: float,
    learning_rate: float = 0.01,
    iterations: int = 2000,
    tolerance: float = 1e-9
) -> float:
    
    current_x = start_x
    for _ in range(iterations):
        gradient = grad_func(current_x)
        step = learning_rate * gradient
        
        
        if abs(step) < tolerance:
            break
            
        current_x += step
        
    return current_x

def find_global_maximum(
    func: Callable[[float], float],
    grad_func: Callable[[float], float],
    bounds: Tuple[float, float],
    num_restarts: int = 100
) -> float:
    
    best_x = float('nan')
    best_y = float('-inf')

    for _ in range(num_restarts):
        
        start_point = random.uniform(bounds[0], bounds[1])
        
        
        candidate_x = gradient_ascent(grad_func, start_point)
        
        
        candidate_x = max(min(candidate_x, bounds[1]), bounds[0])
        candidate_y = func(candidate_x)

        
        if candidate_y > best_y:
            best_y = candidate_y
            best_x = candidate_x

    return best_x

def test_algorithm():
    
    f = lambda x: -(x**2) + 10
    df = lambda x: -2 * x
    
    
    result = find_global_maximum(f, df, (-10.0, 10.0))
    
    
    assert abs(result - 0.0) < 1e-5
    print("Self-test passed: Global maximum found correctly for simple parabola.")

if __name__ == "__main__":
    
    
    def objective(x: float) -> float:
        return math.sin(x) + math.sin(2 * x)

    def gradient(x: float) -> float:
        return math.cos(x) + 2 * math.cos(2 * x)

    search_range = (0, 2 * math.pi)
    
    
    global_max_x = find_global_maximum(objective, gradient, search_range)
    
    print(f"Search Range: {search_range}")
    print(f"Discovered Global Maximum at x: {global_max_x:.6f}")
    print(f"Function value at maximum: {objective(global_max_x):.6f}")
    
    
    test_algorithm()