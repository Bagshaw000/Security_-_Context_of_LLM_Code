import itertools
import math

def pick_coins(probabilities):
    n = len(probabilities) // 2
    best_probability = 0
    best_coins = []

    for coins in itertools.combinations(range(2*n), n):
        probability = 1
        for i in range(2*n):
            if i in coins:
                probability *= probabilities[i]
            else:
                probability *= (1 - probabilities[i])
        if probability > best_probability:
            best_probability = probability
            best_coins = coins

    return best_coins