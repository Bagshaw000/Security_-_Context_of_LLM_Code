import chess

def evaluate_position(board):
    material_score = 0
    for piece in board.piece_map().values():
        if piece.color == chess.WHITE:
            material_score += {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}.get(piece.symbol().lower(), 0)
        else:
            material_score -= {'p': 1, 'n': 3, 'b': 3, 'r': 5, 'q': 9}.get(piece.symbol().lower(), 0)
    
    return material_score