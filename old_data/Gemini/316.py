import unittest

def sort_strings(items):
    
    if not isinstance(items, list):
        raise TypeError("Input must be a list of strings.")
    
    if not all(isinstance(item, str) for item in items):
        raise TypeError("All elements in the list must be strings.")

    return sorted(items)

class TestStringSorter(unittest.TestCase):
    def test_basic_sort(self):
        inventory = ["sensor", "bracket", "actuator", "cable"]
        expected = ["actuator", "bracket", "cable", "sensor"]
        self.assertEqual(sort_strings(inventory), expected)

    def test_empty_list(self):
        self.assertEqual(sort_strings([]), [])

    def test_case_sensitivity(self):
        
        items = ["apple", "Banana", "cherry"]
        expected = ["Banana", "apple", "cherry"]
        self.assertEqual(sort_strings(items), expected)

    def test_invalid_input(self):
        with self.assertRaises(TypeError):
            sort_strings([1, 2, 3])

if __name__ == "__main__":
    
    inventory_items = ["S3 Bucket", "EC2 Instance", "Lambda Function", "DynamoDB Table"]
    sorted_inventory = sort_strings(inventory_items)
    print(f"Sorted Inventory List: {sorted_inventory}")

    
    print("\nRunning unit tests...")
    unittest.main(exit=False)