import numpy as np

class GlobalGradientAscent:
    

    def __init__(self, learning_rate=0.01, max_iterations=1000, convergence_tol=1e-8, restarts=25):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.convergence_tol = convergence_tol
        self.restarts = restarts

    def find_global_maximum(self, objective_func, gradient_func, domain_bounds):
        
        best_overall_x = None
        best_overall_val = -np.inf

        for _ in range(self.restarts):
            
            current_x = np.random.uniform(domain_bounds[0], domain_bounds[1])
            
            for i in range(self.max_iterations):
                gradient = gradient_func(current_x)
                
                
                next_x = current_x + self.learning_rate * gradient
                
                
                next_x = np.clip(next_x, domain_bounds[0], domain_bounds[1])
                
                
                if np.abs(next_x - current_x) < self.convergence_tol:
                    break
                
                current_x = next_x
            
            
            final_val = objective_func(current_x)
            if final_val > best_overall_val:
                best_overall_val = final_val
                best_overall_x = current_x

        return best_overall_x

def objective_function(x):
    
    return np.sin(x) + np.sin(0.3 * x) + np.cos(1.2 * x)

def gradient_function(x):
    
    return np.cos(x) + 0.3 * np.cos(0.3 * x) - 1.2 * np.sin(1.2 * x)

if __name__ == "__main__":
    
    optimizer = GlobalGradientAscent(
        learning_rate=0.05, 
        max_iterations=2000, 
        restarts=50
    )
    
    
    bounds = (-10, 10)
    
    
    max_x = optimizer.find_global_maximum(objective_function, gradient_function, bounds)
    max_val = objective_function(max_x)
    
    print(f"Optimization complete.")
    print(f"Approximate Global Maximum found at x: {max_x:.6f}")
    print(f"Function value at maximum: {max_val:.6f}")