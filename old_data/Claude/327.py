def sort_strings(strings):
    return sorted(strings, key=lambda x: [ord(c) for c in x])