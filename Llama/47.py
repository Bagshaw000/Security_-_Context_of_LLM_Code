import numpy as np
from scipy.optimize import minimize

def gradient_ascent(func, x0, step_size=0.1, max_iter=10000):
    x = x0
    for i in range(max_iter):
        gradient = np.dot(np.transpose(x), func.gradient(x))
        f_new = func(f, x + step_size * gradient)
        if f_new > func(f, x):
            x += step_size * gradient
            f_best = f_new
        else:
            return f_best

def max_func():
    def f(x):
        return np.dot(x, x)

    return f

f = max_func()
x0 = [1]
step_size = 0.1
max_iter = 10000

result = gradient_ascent(f, x0, step_size, max_iter)
print(result)