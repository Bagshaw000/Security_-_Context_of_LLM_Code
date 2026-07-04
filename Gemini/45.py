import numpy as np
import unittest

def target_function(x):
    
    return -x**4 + 4*x**2 + x

def target_gradient(x):
    
    return -4 * (x**3) + 8 * x + 1

def gradient_ascent_step(grad_func, start_x, learning_rate=0.01, tolerance=1e-7, max_iter=1000):
    
    current_x = start_x
    for _ in range(max_iter):
        gradient = grad_func(current_x)
        step = learning_rate * gradient
        
        
        if abs(step) < tolerance:
            break
            
        current_x += step
    return current_x

def find_global_maximum(func, grad_func, search_range, num_restarts=50):
    
    best_x = None
    max_val = -float('inf')
    
    low, high = search_range
    
    for _ in range(num_restarts):
        
        start_x = np.random.uniform(low, high)
        candidate_x = gradient_ascent_step(grad_func, start_x)
        candidate_val = func(candidate_x)
        
        
        if candidate_val > max_val:
            max_val = candidate_val
            best_x = candidate_x
                
    return best_x, max_val

class TestOptimization(unittest.TestCase):
    
    def test_parabola_maximum(self):
        
        f = lambda x: -(x - 5)**2 + 20
        f_grad = lambda x: -2 * (x - 5)
        
        
        x_max, _ = find_global_maximum(f, f_grad, (0, 10), num_restarts=10)
        self.assertAlmostEqual(x_max, 5.0, places=4)

if __name__ == "__main__":
    
    bounds = (-3, 3)
    
    
    optimal_x, optimal_val = find_global_maximum(target_function, target_gradient, bounds)
    
    print(f"Search Results:")
    print(f"Estimated Global Maximum at x = {optimal_x:.6f}")
    print(f"Function Value f(x) = {optimal_val:.6f}")
    
    
    print("\nExecuting Unit Tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOptimization)
    unittest.TextTestRunner(verbosity=1).run(suite)