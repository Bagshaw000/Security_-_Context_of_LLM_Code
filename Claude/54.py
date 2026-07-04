import itertools

def highest_probability_n_heads(probabilities):
    n = len(probabilities) // 2
    coins = list(range(2*n))
    max_probability = 0
    best_selection = []
    
    for selection in itertools.combinations(coins, n):
        probability = 1
        for i in range(2*n):
            if i in selection:
                probability *= probabilities[i]
            else:
                probability *= 1 - probabilities[i]
        if probability > max_probability:
            max_probability = probability
            best_selection = selection
    
    return best_selection