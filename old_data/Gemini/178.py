



white_pawns = 8
white_knights = 2
white_bishops = 2
white_rooks = 2
white_queens = 1


black_pawns = 8
black_knights = 2
black_bishops = 2
black_rooks = 2
black_queens = 1


pawn_value = 1
knight_value = 3
bishop_value = 3
rook_value = 5
queen_value = 9


white_total = (white_pawns * pawn_value) + \
              (white_knights * knight_value) + \
              (white_bishops * bishop_value) + \
              (white_rooks * rook_value) + \
              (white_queens * queen_value)


black_total = (black_pawns * pawn_value) + \
              (black_knights * knight_value) + \
              (black_bishops * bishop_value) + \
              (black_rooks * rook_value) + \
              (black_queens * queen_value)



evaluation = white_total - black_total

print("--- Chess Position Evaluation ---")
print("White Total Material:", white_total)
print("Black Total Material:", black_total)
print("Final Score:", evaluation)

if evaluation > 0:
    print("Status: White has the material advantage.")
elif evaluation < 0:
    print("Status: Black has the material advantage.")
else:
    print("Status: The material is equal.")