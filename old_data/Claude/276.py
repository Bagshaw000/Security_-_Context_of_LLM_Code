import itertools

def find_optimal_coins(n):
    coins = [(i/100.0, 1-i/100.0) for i in range(1, 2*n+1)]
    max_prob = 0
    optimal_coins = None
    for combo in itertools.combinations(coins, n):
        prob = 1
        for p_heads, p_tails in combo:
            prob *= p_heads
        for p_heads, p_tails in coins:
            if (p_heads, p_tails) not in combo:
                prob *= p_tails
        if prob > max_prob:
            max_prob = prob
            optimal_coins = combo
    return optimal_coins