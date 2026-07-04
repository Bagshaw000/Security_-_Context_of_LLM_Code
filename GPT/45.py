def gradient_ascent(func, grad_func, initial_point, learning_rate=0.01, tolerance=1e-6, max_iterations=1000):
    point = initial_point
    for _ in range(max_iterations):
        gradient = grad_func(point)
        new_point = point + learning_rate * gradient
        
        if abs(func(new_point) - func(point)) < tolerance:
            break
        
        point = new_point
        
    return point


def example_function(x):
    return -1 * (x - 2) ** 2 + 3

def example_gradient(x):
    return -2 * (x - 2)

initial_point = 0
maximum = gradient_ascent(example_function, example_gradient, initial_point)
print("Global maximum at:", maximum)