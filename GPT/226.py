def gradient_ascent(func, grad_func, initial_point, learning_rate=0.01, max_iterations=1000, tolerance=1e-6):
    point = initial_point
    for _ in range(max_iterations):
        gradient = grad_func(point)
        new_point = point + learning_rate * gradient
        
        if abs(func(new_point) - func(point)) < tolerance:
            break
        
        point = new_point
    
    return point, func(point)


import numpy as np

def func(x):
    return -1 * (x[0]**2 + x[1]**2)

def grad_func(x):
    return np.array([-2 * x[0], -2 * x[1]])

initial_point = np.array([1.0, 1.0])
max_point, max_value = gradient_ascent(func, grad_func, initial_point)
print("Maximum point:", max_point)
print("Maximum value:", max_value)