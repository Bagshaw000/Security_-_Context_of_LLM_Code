from typing import List

def sort_strings(strings: List[str]) -> List[str]:
    
    return sorted(strings)

def test_sort_strings():
    
    test_data = ["inventory", "aws", "python", "bristol"]
    expected = ["aws", "bristol", "inventory", "python"]
    assert sort_strings(test_data) == expected

if __name__ == "__main__":
    test_sort_strings()