import numpy as np

def gradient_ascent(f, x0, step_size=0.01, max_iterations=1000, tolerance=1e-6):
    x = x0
    for i in range(max_iterations):
        grad = np.gradient(f(x))
        x += step_size * grad
        if np.linalg.norm(grad) < tolerance:
            break
    return x