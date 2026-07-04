



def find_best_coins(coin_list):
    
    
    sorted_probabilities = sorted(coin_list, reverse=True)
    
    
    total_given = len(coin_list)
    n = total_given // 2
    
    
    best_set = sorted_probabilities[:n]
    
    
    
    total_probability = 1.0
    for p in best_set:
        total_probability *= p
        
    return best_set, n, total_probability



my_coins = [0.15, 0.88, 0.42, 0.75