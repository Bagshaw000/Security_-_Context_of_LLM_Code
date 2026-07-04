import itertools

def coin_toss_probability(probabilities):
    n = len(probabilities) // 2
    coins = list(itertools.combinations(probabilities, n))
    max_probability = 0
    optimal_set = None
    for coin_set in coins:
        probability = 1
        for p in coin_set:
            probability *= p
        for p in (1 - p for p in probabilities if p not in coin_set):
            probability *= p
        if probability > max_probability:
            max_probability = probability
            optimal_set = coin_set
    return list(optimal_set)