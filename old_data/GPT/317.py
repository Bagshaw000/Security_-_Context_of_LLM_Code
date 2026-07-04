def sort_strings(strings):
    return sorted(strings, key=lambda s: [ord(char) for char in s])