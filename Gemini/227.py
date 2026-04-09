import numpy as np
import unittest

def gradient_ascent(gradient_fn, start_point, step_size=0.01, iterations=1000, tol=1e-9):
    
    current_x = np.array(start_point, dtype=float)
    for _ in range(iterations):
        gradient = np.array(gradient_fn(current_x))
        update = step_size * gradient
        
        
        if np.linalg.norm(update) < tol:
            break
            
        current_x += update
        
    return current_x

def find_global_maximum(objective_fn, gradient_fn, bounds, n_restarts=100):
    
    best_x = None
    best_val = -np.inf
    
    lower_bound, upper_bound = bounds
    
    for _ in range(n_restarts):
        
        starting_point = np.random.uniform(lower_bound, upper_bound)
        
        
        candidate_x = gradient_ascent(gradient_fn, starting_point)
        candidate_val = objective_fn(candidate_x)
        
        
        if candidate_val > best_val:
            best_val = candidate_val
            best_x = candidate_x
            
    return best_x, best_val


def sample_objective(x):
    
    return -((x**2 - 9)**2) + 2 * x

def sample_gradient(x):
    
    return -4 * x * (x**2 - 9) + 2

class TestOptimization(unittest.TestCase):
    
    def test_concave_maxima(self):
        
        obj = lambda x: -(x**2)
        grad = lambda x: -2*x
        x_max, _ = find_global_maximum(obj, grad, (-10, 10), n_restarts=20)
        self.assertAlmostEqual(float(x_max), 0.0, places=4)

    def test_known_function(self):
        
        x_max, _ = find_global_maximum(sample_objective, sample_gradient, (-5, 5))
        
        self.assertTrue(3.0 < x_max < 3.1)

if __name__ == "__main__":
    
    np.random.seed(42)
    
    
    search_range = (-5, 5)
    
    
    best_point, best_value = find_global_maximum(sample_objective, sample_gradient, search_range)
    
    print(f"Global Maximum found at x = {best_point:.6f}")
    print(f"Objective function value at maximum = {best_value:.6f}")
    
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestOptimization)
    unittest.TextTestRunner(verbosity=1).run(suite)