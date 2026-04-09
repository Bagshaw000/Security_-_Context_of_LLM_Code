import itertools

def solve_max_heads_prob(coin_probs, n):
    
    
    coin_probs.sort()
    
    num_total = len(coin_probs)
    target_heads = n // 2
    
    best_prob = -1.0
    best_subset = []
    
    
    
    for k in range(n + 1):
        
        subset = coin_probs[:k] + coin_probs[num_total - (n - k):]
        
        
        
        dp = [0.0] * (target_heads + 1)
        dp[0] = 1.0
        
        for p in subset:
            for j in range(target_heads, 0, -1):
                dp[j] = dp