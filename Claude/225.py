import numpy as np

def gradient_ascent(f, x0, step_size, max_iterations, tolerance):
    x = x0
    for i in range(max_iterations):
        grad = np.gradient(f(x))
        x_new = x + step_size * grad
        if np.linalg.norm(x_new - x) < tolerance:
            break
        x = x_new
    return x