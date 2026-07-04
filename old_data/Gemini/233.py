import numpy as np

class GradientAscentOptimizer:
    
    
    def __init__(self, learning_rate=0.01, max_iterations=1000, tolerance=1e-8, num_restarts=25):
        
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.num_restarts = num_restarts

    def find_global_maximum(self, objective_func, gradient_func, bounds):
        
        bounds = np.array(bounds)
        dim = bounds.shape[0]
        global_best_params = None
        global_max_value = -np.inf

        for restart in range(self.num_restarts):
            
            current_params = np.random.uniform(bounds[:, 0], bounds[:, 1])
            
            for i in range(self.max_iterations):
                gradient = np.array(gradient_func(current_params))
                
                
                next_params = current_params + self.learning_rate * gradient
                
                
                next_params = np.clip(next_params, bounds[:, 0], bounds[:, 1])
                
                
                if np.linalg.norm(next_params - current_params) < self.tolerance:
                    break
                
                current_params = next_params
            
            
            current_value = objective_func(current_params)
            
            
            if current_value > global_max_value:
                global_max_value = current_value
                global_best_params = current_params

        return global_best_params, global_max_value

def example_complex_objective(x):
    
    return np.sin(x[0]) + np.sin((10.0/3.0) * x[0])

def example_complex_gradient(x):
    
    return [np.cos(x[0]) + (10.0/3.0) * np.cos((10.0/3.0) * x[0])]

if __name__ == "__main__":
    
    search_bounds = [(-5, 5)]
    
    
    
    optimizer = GradientAscentOptimizer(
        learning_rate=0.05, 
        max_iterations=500, 
        num_restarts=50
    )
    
    
    best_x, max_f = optimizer.find_global_maximum(
        example_complex_objective, 
        example_complex_gradient, 
        search_bounds
    )
    
    print(f"Global Maximum located at x: {best_x}")
    print(f"Maximum function value: {max_f}")