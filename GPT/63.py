def sort_strings(strings):
    return sorted(strings, key=lambda s: (s.lower(), s))


strings = ["banana", "Apple", "cherry", "apple"]
sorted_strings = sort_strings(strings)
print(sorted_strings)