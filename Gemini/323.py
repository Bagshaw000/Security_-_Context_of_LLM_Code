from typing import List

def sort_strings_by_custom_order(strings: List[str], order: str) -> List[str]:
    
    
    rank_map = {char: index for index, char in enumerate(order)}
    
    
    
    default_rank = len(order)

    def transform_to_ranks(word: str) -> List[int]:
        
        return [rank_map.get(char, default_rank) for char in word]

    return sorted(strings, key=transform_to_ranks)


if __name__ == "__main__":
    
    custom_alphabet = "zyxwvutsrqponmlkjihgfedcba"
    test_strings = ["apple", "apply", "banana", "bandana", "cherry"]
    
    sorted_results = sort_strings_by_custom_order(test_strings, custom_alphabet)
    print(f"Custom Sorted Order: {sorted_results}")