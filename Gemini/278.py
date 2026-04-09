import numpy as np

def solve():
    def get_prob_exactly_n_heads(probs, n):
        
        k = len(probs)
        if n > k:
            return 0.0
        
        
        dp = [0.0] * (n + 1)
        dp[0] = 1.0
        
        for p in probs:
            for j in range(n, 0, -1):
                dp[j] = dp[j] * (1 - p) + dp[j - 1] * p
            dp[0] = dp[0] * (1 - p)
            
        return dp[n]

    def find_best_subset(all_probs, target_n):
        
        all_probs.sort()
        num_coins = len(all_probs)
        max_probability = -1.0
        best_subset = []

        