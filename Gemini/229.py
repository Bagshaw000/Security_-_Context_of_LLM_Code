import numpy as np

def target_function(x):
    
    return -((x - 2) ** 2) + 10 + 5 * np.sin(2 * x)

def target_gradient(x):
    
    return -2 * (x - 2) + 10 * np.cos(2 * x)

def gradient_ascent_step(grad_fn, start_x, learning_rate=0.01, n_iterations=1000, tolerance=1e-8):
    
    current_x = start_x
    for _ in range(n_iterations):
        
        gradient = grad_fn(current_x)
        step = learning_rate * gradient
        
        
        if abs(step) < tolerance:
            break
            
        
        current_x += step
        
    return current_x

def find_global_maximum(func, grad_fn, bounds, num_restarts=100):
    
    best_x = None
    max_val = -float('inf')
    
    lower_bound, upper_bound = bounds
    
    
    for _ in range(num_restarts):
        
        random_start = np.random.uniform(lower_bound, upper_bound)
        
        
        candidate_x = gradient_ascent_step(grad_fn, random_start)
        
        
        candidate_x = np.clip(candidate_x, lower_bound, upper_bound)
        
        
        candidate_val = func(candidate_x)
        
        
        if candidate_val > max_val:
            max_val = candidate_val
            best_x = candidate_x
            
    return best_x, max_val

def test_global_maximum():
    
    bounds = (-10, 10)
    x_opt, f_opt = find_global_maximum(target_function, target_gradient, bounds)
    
    assert x_opt is not None
    print(f"Global Maximum found at x = {x_opt:.5f}")
    print(f"Maximum function value = {f_opt:.5f}")

if __name__ == "__main__":
    
    np.random.seed(42)
    
    
    test_global_maximum()