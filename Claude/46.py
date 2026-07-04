import numpy as np

def gradient_ascent(func, x0, lr=0.01, max_iter=100, tol=1e-6):
    
    x = x0.copy()
    for i in range(max_iter):
        grad = np.gradient(func(x))
        x += lr * grad
        if np.linalg.norm(grad) < tol:
            break
    return x