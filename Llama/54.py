import numpy as np
from scipy.stats import binom

def optimal_coin_selection(n, p):
    
    coins = [list(range(1, n+1)) for n in range(2, 2*n+1)]
    
    
    max_prob = 0
    opt_comb = None
    
    
    for comb in coins:
        prob = binom.pmf(comb[:n], 2*n, p)
        if prob > max_prob:
            max_prob = prob
            opt_comb = comb
            
    return opt_comb, max_prob

def main():
    n = int(input("Enter the number of coins: "))
    p = float(input("Enter the probability of heads for each coin (0-1): "))
    
    opt_comb, prob = optimal_coin_selection(n, p)
    print(f"Optimal combination: {opt_comb}")
    print(f"Maximum probability: {prob}")

if __name__ == "__main__":
    main()