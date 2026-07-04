import math
import unittest

class GradientAscentError(Exception):
    
    pass

def gradient_ascent(grad_f, initial_x, learning_rate=0.01, max_iters=10000, tolerance=1e-8):
    
    
    
    if not callable(grad_f):
        raise TypeError("The gradient 'grad_f' must be a callable function.")
    
    if not isinstance(max_iters, int):
        raise TypeError("The 'max_iters' parameter must be an integer.")
    if max_iters <= 0:
        raise ValueError("The 'max_iters' parameter must be a positive integer.")
        
    if not isinstance(learning_rate, (int, float)):
        raise TypeError("The 'learning_rate' must be a numeric value.")
    if learning_rate <= 0:
        raise ValueError("The 'learning_rate' must be a positive value.")
        
    if not isinstance(tolerance, (int, float)):
        raise TypeError("The 'tolerance' threshold must be a numeric value.")
    if tolerance <= 0:
        raise ValueError("The 'tolerance' must be a positive value.")
        
    if not isinstance(initial_x, (int, float)):
        raise TypeError("The 'initial_x' starting point must be a numeric value.")

    current_x = float(initial_x)

    for iteration in range(max_iters):
        try:
            
            gradient = grad_f(current_x)
        except Exception as e:
            raise GradientAscentError(f"Error evaluating gradient at x={current_x}: {e}")

        
        if not math.isfinite(gradient):
            raise GradientAscentError(
                f"Numerical instability detected: Gradient is {gradient} at iteration {iteration}."
            )

        step = learning_rate * gradient
        next_x = current_x + step

        
        if not math.isfinite(next_x):
            raise GradientAscentError(
                f"Numerical instability detected: x reached non-finite value {next_x}."
            )

        
        
        if abs(step) < tolerance:
            return next_x

        current_x = next_x

    
    return current_x

class TestGradientAscent(unittest.TestCase):
    

    def test_standard_concave_function(self):
        
        
        def grad_f(x): return -2 * (x - 5)
        result = gradient_ascent(grad_f, initial_x=0.0, learning_rate=0.1)
        self.assertAlmostEqual(result, 5.0, places=6)

    def test_already_at_maximum(self):
        
        def grad_f(x): return 0.0
        result = gradient_ascent(grad_f, initial_x=10.0)
        self.assertEqual(result, 10.0)

    def test_invalid_max_iters(self):
        
        with self.assertRaises(ValueError):
            gradient_ascent(lambda x: 1, 0, max_iters=-10)

    def test_invalid_learning_rate(self):
        
        with self.assertRaises(ValueError):
            gradient_ascent(lambda x: 1, 0, learning_rate=0)

    def test_numerical_overflow_protection(self):
        
        
        def exploding_grad(x): return math.exp(abs(x) + 1.0)
        with self.assertRaises(GradientAscentError):
            gradient_ascent(exploding_grad, initial_x=10.0, learning_rate=1.0)

    def test_nan_gradient_handling(self):
        
        def nan_grad(x): return float('nan')
        with self.assertRaises(GradientAscentError):
            gradient_ascent(nan_grad, initial_x=1.0)

    def test_iteration_limit_enforcement(self):
        
        
        