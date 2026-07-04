import math

def blokus_duo_pieces():
    pieces = []
    for size in range(1, 6):
        for i in range(1, size+1):
            for j in range(i, size+1-i+1):
                pieces.append((i, j))
    pieces = list(set(pieces))
    return pieces

def blokus_duo_possibilities(n):
    pieces = blokus_duo_pieces()
    total_possibilities = 0
    for piece in pieces:
        width, height = piece
        total_possibilities += (n - width + 1) * (n - height + 1) * 4
    return total_possibilities

print(blokus_duo_pieces())
print(blokus_duo_possibilities(5))