def sort_strings_by_custom_order(strings, order):
    
    
    rank_map = {char: index for index, char in enumerate(order)}
    
    def get_sort_key(word):
        
        
        
        return [rank_map.get(char, len(order)) for char in word]
    
    return sorted(strings, key=get_sort_key)




