import itertools

def calculate_exact_heads_prob(coin_probs, target_heads):
    
    n = len(coin_probs)
    if target_heads < 0 or target_heads > n:
        return 0.0
    
    
    dp = [0.0] * (target_heads + 1)
    dp[0] = 1.0
    
    for p in coin_probs:
        for j in range(target_heads, 0, -1):
            dp[j] = dp[j] * (1 - p) + dp[j - 1] * p
        dp[0] *= (1 - p)
        
    return dp[target_heads]

def find_optimal_coin_set(all_probs):
    """
    Given a set of 2n coins, picks a subset of n coins that maximizes 
    the probability of getting exactly n/2 heads.
    
    According to the property of Poisson Binomial Distributions, the 
    optimal subset of size n to maximize the probability of the median 
    outcome (n/2) consists of the 'k' smallest and 'n-k' largest 
    probabilities from the sorted pool of 2n coins.