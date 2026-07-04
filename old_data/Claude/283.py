import random

def pick_coins(probabilities):
    n = len(probabilities) // 2
    coins = [i for i in range(2 * n)]
    selected_coins = random.sample(coins, n)
    return selected_coins

def toss_coins(selected_coins, probabilities):
    heads = 0
    for coin in selected_coins:
        if random.random() < probabilities[coin]:
            heads += 1
    return heads

def find_highest_probability(probabilities):
    max_probability = 0
    best_coins = []
    for i in range(10000):
        selected_coins = pick_coins(probabilities)
        heads = toss_coins(selected_coins, probabilities)
        if heads == len(probabilities) // 2:
            probability = 1
            for j in range(len(probabilities)):
                if j in selected_coins:
                    probability *= probabilities[j]
                else:
                    probability *= 1 - probabilities[j]
            if probability > max_probability:
                max_probability = probability
                best_coins = selected_coins
    return best_coins