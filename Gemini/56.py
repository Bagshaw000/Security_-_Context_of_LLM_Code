def get_best_coins(probabilities):
    
    probabilities.sort()
    
    
    
    
    
    
    
    total_coins = len(probabilities)
    n = total_coins // 2
    
    
    
    
    
    half_n = n // 2
    
    
    smallest_part = probabilities[:half_n]
    
    
    largest_part = probabilities[-half_n:]
    
    
    best_set = smallest_part + largest_part
    
    return best_set


