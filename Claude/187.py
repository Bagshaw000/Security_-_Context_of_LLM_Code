n_squares = [1, 2, 3, 4, 5]
piece_counts = [1, 1, 2, 2, 5]
possibilities = [1, 2, 6, 12, 24]

for i in range(len(n_squares)):
    print(f"Pieces with {n_squares[i]} squares: {piece_counts[i]}")
    print(f"Possibilities for {n_squares[i]}-square pieces: {possibilities[i]}")