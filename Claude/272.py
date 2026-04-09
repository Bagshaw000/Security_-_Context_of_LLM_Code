import numpy as np

def max_probability_n_heads(p, n):
    coins = np.array(p)
    coins.sort()
    
    probability = np.prod(coins[:n]) * np.prod(1 - coins[n:])
    return probability