from itertools import combinations

def max_probability_coins(coins, n):
    def probability_of_heads(selected_coins):
        total_prob = 0
        for heads_count in range(n + 1):
            prob = 1
            for coin in selected_coins:
                prob *= coin[0] if heads_count > 0 else (1 - coin[0])
                heads_count -= 1
            total_prob += prob
        return total_prob

    best_combination = None
    max_prob = 0

    for combo in combinations(coins, n):
        current_prob = probability_of_heads(combo)
        if current_prob > max_prob:
            max_prob = current_prob
            best_combination = combo

    return best_combination



