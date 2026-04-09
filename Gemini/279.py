import numpy as np

def maximize_probability_of_n_heads(probabilities, n):
    
    
    
    
    
    
    probs = sorted(probabilities)
    num_available = len(probs)
    
    def calculate_prob_of_k_heads(subset, k):
        """
        Standard DP to find the probability of getting exactly k heads
        given a list of probabilities (Poisson Binomial Distribution).
