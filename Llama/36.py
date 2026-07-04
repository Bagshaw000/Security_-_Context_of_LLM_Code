import itertools
import math

def is_rectangle(piece):
    return len(set((0, 0), (0, 1), (1, 0), (1, 1))) == 3 and piece != (2, 2)

pieces = {
    (1, 1): 1,
    (1, 2): 1,
    (2, 2): 2,
    (1, 3): 2 if is_rectangle((1, 3)) else 4,
    (2, 3): 4,
    (3, 3): 10,
    (2, 4): 8,
    (3, 4): 12,
    (4, 4): 20,
    (3, 5): 30,
    (4, 5): 40
}

def get_pieces_with_n_squares(n):
    pieces_with_n = []
    for piece in pieces:
        if len(piece) == n:
            pieces_with_n.append(piece)
    return pieces_with_n

def count_pieces_and_possibilities():
    total_pieces = 0
    possibilities = 1
    for i in range(1, 6):
        n_squares_pieces = get_pieces_with_n_squares(i)
        if len(n_squares_pieces) > 0:
            total_pieces += len(n_squares_pieces)
            possibilities *= (i + 1) * math.factorial(len(n_squares_pieces))
    return total_pieces, possibilities

total_pieces, possibilities = count_pieces_and_possibilities()
print(f'Total pieces: {total_pieces}, Possibilities: {possibilities}')