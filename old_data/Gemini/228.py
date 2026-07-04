def objective_function(x):
    
    return -((x - 5) ** 2) + 10

def compute_gradient(x):
    
    return -2 * (x - 5)

def gradient_ascent(start_x, learning_rate=0.1, precision=1e-6, max_iterations=1000):
    
    current_x = start_x
    
    for i in range(max_iterations):
        gradient = compute_gradient(current_x)
        step = learning_rate * gradient
        
        
        current_x += step
        
        
        if abs(step) < precision:
            break
            
    return current_x

def test_ascent_convergence():
    
    start_val = 0.0
    expected = 5.0
    result = gradient_ascent(start_val)
    
    
    assert abs(result - expected) < 1e-4, f"Test failed: Expected {expected}, got {result}"
    print("Unit test passed: Converged to the global maximum.")

if __name__ == "__main__":
    
    initial_guess = -10.0
    alpha = 0.05
    
    
    best_x = gradient_ascent(initial_guess, learning_rate=alpha)
    best_y = objective_function(best_x)
    
    print(f"Starting Point: x = {initial_guess}")
    print(f"Optimization Results:")
    print(f"x_max = {best_x:.5f}")
    print(f"f(x_max) = {best_y:.5f}")
    
    
    test_ascent_convergence()