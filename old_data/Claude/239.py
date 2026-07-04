import numpy as np

def gradient_ascent(func, x0, learning_rate, max_iter):
    
    x = x0.copy()
    
    for i in range(max_iter):
        grad = np.gradient(func(x))
        x += learning_rate * grad
    
    return x