def sort_strings(string_list):
    
    if not all(isinstance(item, str) for item in string_list):
        raise ValueError("All items in the list must be strings.")
    
    return sorted(string_list)

def test_sort_strings():
    
    sample_data = ["AWS", "Python", "Bristol", "inventory", "startup"]
    expected_output = ["AWS", "Bristol", "Python", "inventory", "startup"]
    
    result = sort_strings(sample_data)
    assert result == expected_output, f"Test failed: expected {expected_output}, got {result}"
    print("Unit test passed successfully.")

if __name__ == "__main__":
    
    inventory_items = ["server_rack", "ethernet_cable", "power_supply", "access_point"]
    sorted_items = sort_strings(inventory_items)
    print(f"Sorted Inventory: {sorted_items}")
    
    
    test_sort_strings()