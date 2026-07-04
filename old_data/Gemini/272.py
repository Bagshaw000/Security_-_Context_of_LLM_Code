import numpy as np

def calculate_poisson_binomial_prob(probs, target_heads):
    
    n = len(probs)
    if target_heads > n:
        return 0.0
    
    
    dp = np.zeros((n + 1, target_heads + 1))
    dp[0][0] = 1.0
    
    for i in range(1, n + 1):
        p = probs[i-1]
        for j in range(target_heads + 1):
            
            dp[i][j] = dp[i-1][j] * (1 - p)
            
            if j > 0:
                dp[i][j] += dp[i-1][j-1] * p
                
    return dp[n][target_heads]

def find_optimal_subset(coin_probs):
    """
    Given 2n coins, finds a subset of size n that maximizes the probability 
    of getting exactly n/2 heads.
    
    Note: Based on the statistical property that to maximize