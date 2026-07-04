def natural_sort_key(s):
    return sorted(s.replace('-', ' ').replace('_', ' ').split())

def sort_strings(strings):
    return sorted(strings, key=natural_sort_key)

print(sort_strings(['hello-world', 'world', 'hello', 'hell-ow']))  