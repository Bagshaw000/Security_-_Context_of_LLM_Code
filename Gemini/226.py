import math
import random
import unittest

def target_function(x):
    
    return math.sin(x) - 0.01 * (x ** 2)

def target_gradient(x):
    
    return math.cos(x) - 0.02 * x

def gradient_ascent_step(start_x, learning_rate=0.1, max_iterations=1000, tolerance=1e-8):
    
    current_x = start_x
    for _ in range(max_iterations):
        gradient = target_gradient(current_x)
        next_x = current_x + (learning_rate * gradient)
        
        
        if abs(next_x - current_x) < tolerance:
            break
        current_x = next_x
    return current_x

def find_global_maximum(search_range=(-20, 20), num_restarts=50):
    
    best_x = None
    max_value = float('-inf')

    for _ in range(num_restarts):
        
        random_start = random.uniform(search_range[0], search_range[1])
        
        
        local_max_x = gradient_ascent_step(random_start)
        local_max_val = target_function(local_max_x)

        
        if local_max_val > max_value:
            max_value = local_max_val
            best_x = local_max_x

    return best_x, max_value

class TestOptimization(unittest.TestCase):
    
    def test_improvement(self):
        
        start_x = 0
        start_val = target_function(start_x)
        optimized_x, optimized_val = find_global_maximum(search_range=(-5, 5), num_restarts=10)
        self.assertGreaterEqual(optimized_val, start_val)

    def test_known_peak(self):
        
        _, max_val = find_global_maximum()
        
        self.assertGreater(max_val, 0.9)

if __name__ == "__main__":
    
    x_opt, y_opt = find_global_maximum()
    
    print(f"--- Gradient Ascent Optimization ---")
    print(f"Global Maximum found at x: {x_opt:.6f}")
    print(f"Function value at maximum: {y_opt:.6f}")
    
    
    print("\n--- Running Unit Tests ---")
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromTestCase(TestOptimization)
    runner = unittest.TextTestRunner(verbosity=1)
    runner.run(suite)