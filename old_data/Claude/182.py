import itertools

def blokus_duo_pieces():
    pieces = []
    for i in range(1, 6):
        for combo in itertools.combinations([(0,0)] * i, i):
            piece = set(combo)
            if piece not in pieces:
                pieces.append(piece)
    return pieces

def blokus_duo_possibilities():
    pieces = blokus_duo_pieces()
    return len(pieces)

print(len(blokus_duo_pieces()))
print(blokus_duo_possibilities())