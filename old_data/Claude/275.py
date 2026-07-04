import numpy as np
from itertools import combinations

def coin_toss_probability(coins):
    n = len(coins) // 2
    probabilities = []
    for subset in combinations(coins, n):
        p_heads = np.prod(subset)
        p_tails = np.prod(1 - np.array(subset))
        probabilities.append(p_heads * p_tails)
    return max(probabilities)