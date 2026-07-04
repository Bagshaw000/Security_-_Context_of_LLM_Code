




pawn_value = 1
knight_value = 3
bishop_value = 3
rook_value = 5
queen_value = 9



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



white_total = (white_pawns * pawn_value) + (white_knights * knight_value) + (white_bishops * bishop_value) + (white_rooks * rook_value) + (white_queens * queen_value)


black_total = (black_pawns * pawn_value) + (black_knights * knight_value) + (black_bishops * bishop_value) + (black_rooks * rook_value) + (black_queens * queen_value)



result = white_total - black_total

print("White's total points:")
print(white_total)

print("Black's total points:")
print(black_total)

print("The position evaluation is (Positive favors White, Negative favors Black):")
print(result)