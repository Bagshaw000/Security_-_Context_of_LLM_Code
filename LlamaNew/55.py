import typing

class CoinSelectionOptimizer:
    

    def __init__(self):
        
        pass

    def _calculate_exact_k_heads_probability(self, probabilities: typing.List[float], k: int) -> float:
        
        if k < 0 or k > len(probabilities):
            return 0.0

        
        dp = [0.0] * (k + 1)
        dp[0] = 1.0

        for p in probabilities:
            
            for j in range(k, 0, -1):
                dp[j] = (dp[j] * (1.0 - p)) + (dp[j - 1] * p)
            dp[0] *= (