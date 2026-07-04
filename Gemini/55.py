import numpy as np

def maximize_n_heads_probability(probabilities):
    
    
    n_target = len(probabilities) // 2
    probs = sorted(probabilities, reverse=True)
    
    
    
    def get_prob_of_k_heads(coin_subset, k):
        m = len(coin_subset)
        if k > m:
            return 0
        
        dp = np.zeros((m + 1,