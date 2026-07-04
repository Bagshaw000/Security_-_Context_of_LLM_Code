def sort_strings(strings):
    
    if not isinstance(strings, list):
        raise TypeError("Input must be a list of strings")
    
    return sorted(strings)

if __name__ == "__main__":
    
    system_components = [
        "Remote Key Provisioning",
        "Passkeys",
        "Device Authentication",
        "Account Linking",
        "Device Profiles",
        "Registration"
    ]
    
    sorted_components = sort_strings(system_components)
    print(sorted_components)