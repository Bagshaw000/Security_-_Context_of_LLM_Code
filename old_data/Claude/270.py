import itertools

def find_optimal_coins(n):
    coins = [(i+1)/(2*n) for i in range(2*n)]
    max_probability = 0
    optimal_coins = None
    for combination in itertools.combinations(coins, n):
        probability = 1
        for p in combination:
            probability *= p
        for p in [c for c in coins if c not in combination]:
            probability *= (1-p)
        if probability > max_probability:
            max_probability = probability
            optimal_coins = combination
    return optimal_coins