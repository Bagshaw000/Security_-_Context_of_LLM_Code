def solve():
    def get_prob_exactly_n_heads(subset_probs, n):
        
        
        dp = [0.0] * (n + 1)
        dp[0] = 1.0
        
        for p in subset_probs:
            for j in range(n, 0, -1):
                
                
                
                dp[j] = (dp[j - 1] * p) + (dp[j] * (1 - p))
            
            dp[0] = dp[0] * (1 - p)
            
        return dp[n]

    def find_best_coin_subset(all_probs, n):
        