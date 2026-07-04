def count_blokus_duo_pieces():
    n = 5
    pieces = []
    for i in range(1, n+1):
        for j in range(1, i+1):
            if i * j <= n:
                pieces.append((i, j))
    symmetries = [1, 2, 4, 4, 8]
    return sum(symmetries[i-1] for i in range(1, n+1))