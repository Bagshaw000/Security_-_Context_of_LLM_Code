from typing import List, Iterable, Optional

def sort_strings(strings: Optional[Iterable[str]]) -> List[str]:
    
    if strings is None:
        return []
    
    return sorted(strings)

if __name__ == "__main__":
    
    input_data = ["Brad", "Amazon", "Device Management", "Authentication", "Passkeys", "Remote Key Provisioning"]
    sorted_data = sort_strings(input_data)
    print(sorted_data)