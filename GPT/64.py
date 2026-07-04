def sort_strings(strings):
    return sorted(strings, key=lambda s: (s.lower(), s))


strings = ["Brad", "alice", "Charlie", "bob"]
sorted_strings = sort_strings(strings)
print(sorted_strings)