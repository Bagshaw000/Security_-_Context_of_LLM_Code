import numpy as np

def gradient_ascent(f, x0, lr, tol, max_iter):
    x = x0
    for i in range(max_iter):
        grad = np.gradient(f(x))
        x = x + lr * grad
        if np.linalg.norm(grad) < tol:
            break
    return x