import numpy as np

def optimal_coin_set(p_list):
    n = len(p_list) // 2
    p_list.sort(reverse=True)
    
    optimal_coins = p_list[:n]
    
    prob_n_heads = 0
    for p in optimal_coins:
        prob_n_heads += (n * p * (1-p)**(n-1))
    
    return optimal_coins, prob_n_heads