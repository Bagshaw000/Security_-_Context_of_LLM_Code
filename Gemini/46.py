import numpy as np

class GlobalGradientAscentOptimizer:
    

    def __init__(self, learning_rate=0.01, max_iterations=1000, tolerance=1e-7, n_restarts=25):
        self.learning_rate = learning_rate
        self.max_iterations = max_iterations
        self.tolerance = tolerance
        self.n_restarts = n_restarts

    def _compute_numerical_gradient(self, func, x, epsilon=1e-8):
        
        grad = np.zeros_like(x, dtype=float)
        for i in range(len(x)):
            x_step_plus = np.copy(x).astype(float)
            x_step_minus = np.copy(x).astype(float)
            x_step_plus[i] += epsilon
            x_step_minus[i] -= epsilon
            grad[i] = (func(x_step_plus) - func(x_step_minus)) / (2 * epsilon)
        return grad

    def optimize(self, func, bounds, grad_func=None):
        
        bounds = np.array(bounds)
        dim = len(bounds)
        global_best_x = None
        global_best_val = -np.inf

        for restart in range(self.n_restarts):
            
            current_x = np.random.uniform(bounds[:, 0], bounds[:, 1])
            
            for i in range(self.max_iterations):
                if grad_func:
                    gradient = grad_func(current_x)
                else:
                    gradient = self._compute_numerical_gradient(func, current_x)

                
                next_x = current_x + self.learning_rate * gradient
                
                
                next_x = np.clip(next_x, bounds[:, 0], bounds[:, 1])

                
                if np.linalg.norm(next_x - current_x) < self.tolerance:
                    current_x = next_x
                    break
                
                current_x = next_x

            current_val = func(current_x)

            
            if current_val > global_best_val:
                global_best_val = current_val
                global_best_x = current_x

        return global_best_x, global_best_val

def example_objective(x):
    
    
    
    main_peak = np.exp(-(x[0]**2 + x[1]**2))
    
    local_peak = 0.5 * np.exp(-((x[0]-3)**2 + (x[1]-3)**2))
    return main_peak + local_peak

if __name__ == "__main__":
    
    search_bounds = [(-5, 5), (-5, 5)]
    
    optimizer = GlobalGradientAscentOptimizer(
        learning_rate=0.1, 
        max_iterations=500, 
        n_restarts=15
    )
    
    best_coords, max_value = optimizer.optimize(example_objective, search_bounds)
    
    print(f"Global Maximum found at: {best_coords}")
    print(f"Maximum Value: {max_value}")