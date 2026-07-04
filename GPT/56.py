import itertools

def probability_of_n_heads(coins, n):
    total_probability = 0
    for combination in itertools.combinations(coins, n):
        prob = 1
        for coin in combination:
            prob *= coin
        total_probability += prob
    return total_probability

def best_set_of_coins(coins, n):
    best_probability = 0
    best_combination = None
    for combination in itertools.combinations(coins, n):
        current_probability = probability_of_n_heads(combination, n)
        if current_probability > best_probability:
            best_probability = current_probability
            best_combination = combination
    return best_combination, best_probability


coins = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]  
n = len(coins) // 2
best_combination, best_probability = best_set_of_coins(coins, n)
print("Best combination of coins:", best_combination)
print("Best probability of getting n heads:", best_probability)