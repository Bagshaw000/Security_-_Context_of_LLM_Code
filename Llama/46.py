import numpy as np
import random

def gradient_ascent(func, initial_guess, learning_rate=0.01, max_iter=10000):
    x = initial_guess
    for i in range(max_iter):
        fx = func(x)
        if i % 10 == 0:
            print(f"Iteration {i}: f(x) = {fx:.6f}")
        gradient = np.array([2 * (func(x + epsilon) - func(x)) / epsilon for epsilon in [1e-4, 1e-5, 1e-6]])
        x -= learning_rate * gradient
    return x

def test_func(x):
    return -(x[0]**2 + x[1]**2)

initial_guess = np.array([random.random() for _ in range(2)])
final_answer = gradient_ascent(test_func, initial_guess)