from typing import List

def sort_strings_alphabetically(strings: List[str]) -> List[str]:
    
    
    return sorted(strings)

def test_sorting_function():
    
    sample_input = ["inventory", "aws", "python", "bristol", "software"]
    expected_output = ["aws", "bristol", "inventory", "python", "software"]
    
    result = sort_strings_alphabetically(sample_input)
    
    assert result == expected_output, f"Expected {expected_output}, but got {result}"
    print("Unit test passed: The strings are sorted correctly according to underlying ordering.")

if __name__ == "__main__":
    
    test_sorting_function()
    
    inventory_items = ["Server", "Database", "LoadBalancer", "S3Bucket"]
    sorted_items = sort_strings_alphabetically(inventory_items)
    print(f"Sorted Inventory: {sorted_items}")