def calculate_exactly_n_heads(subset, target):
    dp = [0.0] * (target + 1)
    dp[0] = 1.0
    for p in subset:
        p_inv = 1.0 - p
        for j in range(target, 0, -1):
            dp[j] = dp[j] * p_inv + dp[j - 1] * p
        dp[0] *= p_inv
    return dp[target]

def pick_optimal_coins(coin_probabilities):
    
    total_available = len(coin_probabilities)
    n_target = total_available // 2
    
    if n_target == 0:
        return []

    
    
    sorted_probs = sorted(coin_probabilities)
    
    best_subset = []
    max_prob = -1.0
    
    
    for k in range(n_target, total_available + 1):
        
        