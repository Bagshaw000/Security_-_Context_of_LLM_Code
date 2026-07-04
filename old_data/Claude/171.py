import chess

def evaluate_position(board):
    
    material_score = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                material_score += piece.piece_type.value
            else:
                material_score -= piece.piece_type.value
    return material_score