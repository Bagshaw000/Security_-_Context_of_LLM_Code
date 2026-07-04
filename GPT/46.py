def gradient_ascent(func, grad_func, initial_point, learning_rate=0.01, tolerance=1e-6, max_iterations=1000):
    point = initial_point
    for _ in range(max_iterations):
        gradient = grad_func(point)
        new_point = point + learning_rate * gradient
        
        if abs(func(new_point) - func(point)) < tolerance:
            break
        
        point = new_point
    
    return point


import numpy as np

def func(x):
    return -1 * (x - 2) ** 2 + 3

def grad_func(x):
    return -2 * (x - 2)

initial_point = 0
max_point = gradient_ascent(func, grad_func, initial_point)
print("Global maximum at:", max_point)