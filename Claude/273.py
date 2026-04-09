import itertools

def pick_coins(probs):
    n = len(probs) // 2
    coins = list(range(2*n))
    max_prob = 0
    best_set = []
    for subset in itertools.combinations(coins, n):
        prob = 1
        for i in range(2*n):
            if i in subset:
                prob *= probs[i]
            else:
                prob *= (1 - probs[i])
        if prob > max_prob:
            max_prob = prob
            best_set = subset
    return best_set