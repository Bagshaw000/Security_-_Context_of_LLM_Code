import itertools
from math import sqrt

def is_square(n):
    side = int(sqrt(n))
    return side*side == n

def get_squares(max_size, pieces_used=None):
    if pieces_used is None:
        pieces_used = [1]*max_size + list(range(2, max_size+1))
    else:
        pieces_used = set(pieces_used)

    squares = {piece: 0 for piece in range(1, max_size+1)}
    squares[1] = 1
    squares[4] = 3

    for i in range(2, max_size+1):
        if is_square(i):
            squares[i] = 1

        for j in pieces_used:
            if is_square(j) and j <= i:
                squares[j] += squares[i-j]

    return squares

def calculate_total_pieces(squares):
    total_pieces = sum([squares[i] for i in range(1, len(squares))])
    return total_pieces

def calculate_possibilities(n, max_size=7):
    total_squares = [sum(get_squares(max_size=i)[i]) for i in range(1, n+1)]
    pieces_used_combinations = list(itertools.combinations(range(1, n+1), n))

    possibilities = set()
    for combination in pieces_used_combinations:
        used_squares = {piece: 0 for piece in range(1, len(get_squares(max_size=7)))}
        for i in combination:
            used_squares[i] += get_squares(max_size=7)[i]
        if calculate_total_pieces(used_squares) == n:
            possibilities.add(tuple(sorted(used_squares.items())))

    return possibilities

def main():
    num_pieces = int(input("Enter the number of pieces: "))
    possibilities = calculate_possibilities(num_pieces)
    print("Total squares:", len(possibilities))
    print("Possibilities:")
    for possibility in sorted(list(possibilities)):
        print(possibility)

if __name__ == "__main__":
    main()