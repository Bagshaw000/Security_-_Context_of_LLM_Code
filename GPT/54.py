from itertools import combinations

def max_probability_coins(coins, n):
    def probability_of_heads(selected_coins):
        prob = 0
        for heads in range(n + 1):
            prob_heads = 1
            prob_tails = 1
            for i in range(n):
                if i < heads:
                    prob_heads *= selected_coins[i]
                else:
                    prob_tails *= (1 - selected_coins[i])
            prob += prob_heads * prob_tails
        return prob

    max_prob = 0
    best_combination = None
    for selected in combinations(coins, n):
        current_prob = probability_of_heads(selected)
        if current_prob > max_prob:
            max_prob = current_prob
            best_combination = selected

    return best_combination, max_prob


coins = [0.1, 0.5, 0.7, 0.9]  
n = 2
result = max_probability_coins(coins, n)
print(result)