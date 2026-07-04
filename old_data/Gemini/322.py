from typing import List

def sort_strings(strings: List[str]) -> List[str]:
    
    if not isinstance(strings, list):
        raise TypeError("Input must be a list of strings.")
    
    return sorted(strings)

if __name__ == "__main__":
    
    data = [
        "device-authentication",
        "device-registration",
        "device-profiles",
        "account-linking",
        "Remote Key provisioning",
        "Passkeys"
    ]
    
    sorted_data = sort_strings(data)
    print(sorted_data)