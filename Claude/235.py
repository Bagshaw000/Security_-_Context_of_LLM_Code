import numpy as np

def gradient_ascent(f, x0, learning_rate, max_iterations, tolerance):
    x = x0
    for i in range(max_iterations):
        grad = np.gradient(f(x))
        x_new = x + learning_rate * grad
        if np.linalg.norm(x_new - x) < tolerance:
            break
        x = x_new
    return x