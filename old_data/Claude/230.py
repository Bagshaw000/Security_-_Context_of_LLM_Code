import numpy as np

def gradient_ascent(func, x_init, learning_rate, num_iterations):
    x = x_init
    for i in range(num_iterations):
        gradient = np.gradient(func(x))
        x = x + learning_rate * gradient
    return x