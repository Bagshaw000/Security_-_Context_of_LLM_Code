import numpy as np

def gradient_ascent(f, x0, learning_rate, max_iter, tol):
    x = x0
    for i in range(max_iter):
        grad = f.grad(x)
        x = x + learning_rate * grad
        if np.linalg.norm(grad) < tol:
            break
    return x