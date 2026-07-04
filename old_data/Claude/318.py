def sort_strings(strings):
    return sorted(strings, key=lambda x: (len(x), x))