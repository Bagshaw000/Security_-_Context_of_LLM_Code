import numpy as np
from itertools import combinations

def find_optimal_coins(n, probs):
    n_coins = 2 * n
    best_prob = 0
    best_coins = []
    
    for combo in combinations(range(n_coins), n):
        heads_probs = [probs[i] for i in combo]
        tails_probs = [1 - p for p in heads_probs]
        prob = np.prod(heads_probs) * np.prod(tails_probs)
        if prob > best_prob:
            best_prob = prob
            best_coins = combo
    
    return best_coins