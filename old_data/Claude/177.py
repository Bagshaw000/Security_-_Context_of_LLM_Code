import chess

def evaluate_position(board):
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    score = 0
    for square in range(chess.SQUARE_NAMES):
        piece = board.piece_at(square)
        if piece:
            score += (1 if piece.color == chess.WHITE else -1) * piece_values[piece.symbol().upper()]
    return score