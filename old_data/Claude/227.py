import numpy as np

def gradient_ascent(f, x0, step_size, max_iterations, tolerance):
    x = x0
    for i in range(max_iterations):
        grad = compute_gradient(f, x)
        x_new = x + step_size * grad
        if np.linalg.norm(x_new - x) < tolerance:
            break
        x = x_new
    return x

def compute_gradient(f, x):
    epsilon = 1e-6
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += epsilon
        x_minus = x.copy()
        x_minus[i] -= epsilon
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * epsilon)
    return grad