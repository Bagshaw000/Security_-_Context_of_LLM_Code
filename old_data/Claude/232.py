import numpy as np

def gradient_ascent(f, x_init, learning_rate, max_iter):
    x = x_init
    for i in range(max_iter):
        grad = np.gradient(f(x))
        x = x + learning_rate * grad
    return x