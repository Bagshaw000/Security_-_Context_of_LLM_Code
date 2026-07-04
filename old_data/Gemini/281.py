def find_best_coin_subset(probabilities):
    
    
    

    total_coins = len(probabilities)
    target_heads = total_coins // 2
    
    
    
    sorted_probs = sorted(probabilities)
    
    best_subset = []
    highest_probability = -1.0
    
    
    
    for subset_size in range(target_heads, total_coins + 1):
        
        
        
        
        for count_from_high_end in range(subset_size + 1):
            count_from_low_end = subset_size - count_from_high_end
            
            
            if count_from_