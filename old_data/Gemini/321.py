from typing import List

def sort_strings_by_order(strings: List[str], order: str) -> List[str]:
    
    
    rank_map = {char: index for index, char in enumerate(order)}
    
    def transform_to_rank_list(word: str) -> List[int]:
        
        
        
        return [rank_map.get(char, len(order)) for char in word]
    
    return sorted(strings, key=transform_to_rank_list)

if __name__ == "__main__":
    
    words_to_sort = ["apple", "amazon", "alexa", "kindle", "fire"]
    custom_alphabet = "zyxwvutsrqponmlkjihgfedcba"
    
    sorted_list = sort_strings_by_order(words_to_sort, custom_alphabet)
    print(f"Original: {words_to_sort}")
    print(f"Sorted:   {sorted_list}")