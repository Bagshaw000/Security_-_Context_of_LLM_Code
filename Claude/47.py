import numpy as np

def gradient_ascent(f, start, step_size, tolerance, max_iterations):
    
    x = start
    for i in range(max_iterations):
        grad = np.gradient(f(x))
        x += step_size * grad
        if np.linalg.norm(grad) < tolerance:
            break
    return x