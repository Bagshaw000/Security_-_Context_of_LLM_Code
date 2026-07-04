import itertools

def pick_coins(p_heads):
    n = len(p_heads) // 2
    coins = list(range(2*n))
    max_prob = 0
    best_coins = []
    for combo in itertools.combinations(coins, n):
        prob = 1
        for i in range(2*n):
            if i in combo:
                prob *= p_heads[i]
            else:
                prob *= (1 - p_heads[i])
        if prob > max_prob:
            max_prob = prob
            best_coins = combo
    return best_coins