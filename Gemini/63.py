import re

def get_natural_sort_key(text):
    
    return [int(part) if part.isdigit() else part.lower() 
            for part in re.split(r'(\d+)', text)]

def sort_strings(items):
    
    if not all(isinstance(i, str) for i in items):
        raise TypeError("All items in the input list must be strings.")
    
    return sorted(items, key=get_natural_sort_key)

def test_sort_strings():
    
    test_input = ["item10.png", "item2.png", "item1.png", "20", "2"]
    expected_output = ["2", "20", "item1.png", "item2.png", "item10.png"]
    
    result = sort_strings(test_input)
    assert result == expected_output, f"Expected {expected_output}, but got {result}"

if __name__ == "__main__":
    test_sort_strings()