def find_best_coins(probabilities):
    
    
    
    

    
    total_coins = len(probabilities)
    n = total_coins // 2

    
    
    probabilities.sort(reverse=True)

    
    best_subset = probabilities[:n]

    return best_subset




available_coins = [0.15, 0.85, 0.40, 0.92, 0.22, 0.78]
result = find_best_coins(available_coins)

print("The best coins to pick have these probabilities of heads:")
print(result)