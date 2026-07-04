import itertools
import math

def coin_toss_probability(coin_probabilities):
    n = len(coin_probabilities) // 2
    best_probability = 0
    best_coin_set = []

    for coin_set in itertools.combinations(coin_probabilities, n):
        probability = 1
        for p in coin_set:
            probability *= p
        for p in (1 - x for x in coin_set):
            probability *= p
        if probability > best_probability:
            best_probability = probability
            best_coin_set = coin_set

    return best_probability, best_coin_set