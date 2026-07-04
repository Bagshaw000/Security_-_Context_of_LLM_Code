import numpy as np
from scipy.optimize import minimize

def gradient_ascent(func, x0, learning_rate=0.1, max_iter=1000):
    
    x = x0.copy()
    
    for _ in range(max_iter):
        
        grad = np.gradient(func(x))
        
        
        x += learning_rate * grad
        
    return x