from itertools import combinations

def max_probability_coins(coins, n):
    def probability_of_heads(selected_coins):
        prob = 1
        for coin in selected_coins:
            prob *= coin
        return prob

    max_prob = 0
    best_combination = []

    for combo in combinations(coins, n):
        prob = probability_of_heads(combo)
        if prob > max_prob:
            max_prob = prob
            best_combination = combo

    return best_combination, max_prob


coins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8]  
n = 4  
result = max_probability_coins(coins, n)
print(result)