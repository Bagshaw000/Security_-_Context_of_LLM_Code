from itertools import combinations

def max_probability_coins(coins, n):
    def probability_of_heads(selected_coins):
        total_heads = 0
        total_tosses = 0
        for coin in selected_coins:
            total_heads += coin
            total_tosses += 1
        return total_heads / total_tosses

    best_combination = None
    best_probability = 0

    for combo in combinations(coins, n):
        prob = probability_of_heads(combo)
        if prob > best_probability:
            best_probability = prob
            best_combination = combo

    return best_combination, best_probability


coins = [0.1, 0.5, 0.7, 0.9]  
n = 2
result = max_probability_coins(coins, n)
print(result)