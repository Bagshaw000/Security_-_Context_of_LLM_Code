def sort_strings(input_list):
    
    if not all(isinstance(s, str) for s in input_list):
        raise ValueError("All elements in the list must be strings.")
    
    return sorted(input_list)

def test_sort_strings():
    
    
    assert sort_strings(["banana", "apple", "cherry"]) == ["apple", "banana", "cherry"]
    
    
    assert sort_strings(["zebra", "Apple", "banana"]) == ["Apple", "banana", "zebra"]
    
    
    assert sort_strings([]) == []
    
    print("All unit tests passed.")

if __name__ == "__main__":
    
    inventory_items = ["sensor", "actuator", "bracket", "controller"]
    sorted_inventory = sort_strings(inventory_items)
    
    print(f"Original: {inventory_items}")
    print(f"Sorted: {sorted_inventory}")
    
    
    test_sort_strings()