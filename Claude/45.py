Here is the Python code to implement a gradient ascent algorithm for finding the global maximum of a function:

import numpy as np

def gradient_ascent(f, x_0, learning_rate, tolerance, max_iterations):
    
    x = x_0
    for i in range(max_iterations):
        gradient = grad(f, x)
        x = x + learning_rate * gradient
        if np.linalg.norm(gradient) < tolerance:
            break
    return x

def grad(f, x):
    
    h = 1e-6
    n = len(x)
    grad_f = np.zeros_like(x)
    for i in range(n):
        e = np.zeros(n)
        e[i] = h
        grad_f[i] = (f(x + e) - f(x - e)) / (2 * h)
    return grad_f