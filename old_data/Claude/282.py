import itertools

def find_optimal_coins(n):
    coins = [(i+1)/(2*n), n-i] for i in range(n)]
    max_probability = 0
    optimal_coins = []
    
    for subset in itertools.combinations(coins, n):
        probability = 1
        for p, _ in subset:
            probability *= p
        if probability > max_probability:
            max_probability = probability
            optimal_coins = [c for p, c in subset]
    
    return optimal_coins