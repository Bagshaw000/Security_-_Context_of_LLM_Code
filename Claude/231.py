import numpy as np

def gradient_ascent(f, x0, learning_rate, max_iterations, tolerance):
    x = x0
    for i in range(max_iterations):
        grad = f_prime(f, x)
        x_new = x + learning_rate * grad
        if np.linalg.norm(x_new - x) < tolerance:
            return x_new
        x = x_new
    return x

def f_prime(f, x):
    eps = 1e-6
    grad = np.zeros_like(x)
    for i in range(len(x)):
        x_plus = x.copy()
        x_plus[i] += eps
        x_minus = x.copy()
        x_minus[i] -= eps
        grad[i] = (f(x_plus) - f(x_minus)) / (2 * eps)
    return grad