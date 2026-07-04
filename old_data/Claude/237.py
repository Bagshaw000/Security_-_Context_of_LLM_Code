import numpy as np

def gradient_ascent(f, x0, learning_rate, max_iter):
    
    x = x0
    for _ in range(max_iter):
        grad = np.gradient(f(x))
        x += learning_rate * grad
    return x