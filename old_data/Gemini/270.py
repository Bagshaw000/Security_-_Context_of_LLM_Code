import numpy as np

def solve():
    
    
    
    
    
    coins = [0.1, 0.2, 0.3, 0.7, 0.8, 0.9] 
    coins.sort()
    
    n_total = len(coins)
    n_pick = n_total // 2
    target_heads = n_pick // 2 
    
    def get_prob_exactly_k_heads(subset, k):
        
        m = len(subset)
        dp = [[0] * (k + 1) for _ in range(m