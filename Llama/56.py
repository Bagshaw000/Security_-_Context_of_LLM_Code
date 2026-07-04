import numpy as np
from scipy.stats import binom

def find_best_coins(n, p_values):
    n_coins = 2 * n
    probabilities = []
    for i in range(1 << n_coins):  
        combination = [0] * n_coins
        count = 0
        while i > 0:
            if i & 1:  
                combination[count] += 1
                p = np.mean([p_values[j] for j in range(count, count + len(p_values))])
                probabilities.append(p ** combination[count] * (1 - p) ** (n_coins - combination[count]))
            i >>= 1  
            count += 1
    return max(zip(range(n), probabilities))

n = 3
p_values = [0.6, 0.4, 0.8]
print(find_best_coins(n, p_values))