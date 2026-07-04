def sort_strings(strings):
    return sorted(strings, key=lambda x: [ord(char) for char in x])