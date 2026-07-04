import numpy as np
from scipy.stats import binom

def calculate_coins(coins, n):
    
    p = [1/len(coins)] * len(coins)
    
    def cost_function(p, n):
        return -np.sum([p[i] * np.log2(p[i]) for i in range(len(p))])
    
    
    def simulate_annealing(temperature, p, n, coins):
        T = temperature
        while True:
            change = cost_function(p, n)
            if np.isclose(change, 0) or np.random.rand() > np.exp(-(change - cost_function(p, n)) / T):
                i = np.random.randint(len(coins))
                j = np.random.randint(len(coins))
                p[i], p[j] = p[j], p[i]
            else:
                return
            if temperature < 0.1:
                break
            temperature *= 0.99
    
    
    coins.sort(key=lambda x: np.log2(x[1]))
    cost_function(p, n)
    
    def min_cost(n):
        for i in range(len(coins)):
            p[i] = coins[i][1]
        return cost_function(p, n)
        
    min_n = 0
    max_n = len(coins) // 2
    
    while max_n - min_n > 1:
        mid = (min_n + max_n) // 2
        
        def evaluate_coin(num_coins):
            p = [1/len(coins)] * len(coins)
            
            
            for i in range(len(coins)):
                if coins[i][0] < num_coins:
                    p[i] += (num_coins - coins[i][0]) / (len(coins) * (len(coins)-1))
            
            cost_function(p, mid)
        
        while True:
            evaluate_coin(mid)
            if min_cost(mid) <= min_cost(mid+1):
                max_n = mid
            else:
                min_n = mid
                
    
    chosen_coins = []
    
    for i in range(min_n, min_n + len(coins)//2):
        chosen_coins.append((i, coins[i][1]))
        
    return chosen_coins

coins = [(0.05, 0.01), (0.07, 0.03), (0.09, 0.05)]
print(calculate_coins(coins, 6))