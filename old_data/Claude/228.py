import numpy as np

def gradient_ascent(f, x0, lr=0.01, tol=1e-6, max_iter=1000):
    x = x0
    for i in range(max_iter):
        grad = np.gradient(f(x))
        x += lr * grad
        if np.linalg.norm(grad) < tol:
            break
    return x