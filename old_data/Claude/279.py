import numpy as np

def choose_coins(probabilities):
    n = len(probabilities) // 2
    coins = list(range(2 * n))
    result = []
    for i in range(n):
        max_prob = 0
        best_coin = None
        for j in coins:
            prob = (probabilities[j] ** n) * ((1 - probabilities[j]) ** n)
            if prob > max_prob:
                max_prob = prob
                best_coin = j
        result.append(best_coin)
        coins.remove(best_coin)
    return result