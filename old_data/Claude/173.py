import chess

def evaluate_position(board):
    material_score = 0
    piece_values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9, 'K': 0}
    for square in range(64):
        piece = board.piece_at(square)
        if piece:
            material_score += (piece_values[piece.symbol().upper()] * (1 if piece.color == chess.WHITE else -1))
    return material_score