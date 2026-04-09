import chess

def evaluate_position(board):
    material_score = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            piece_value = 0
            if piece.piece_type == chess.PAWN:
                piece_value = 100
            elif piece.piece_type == chess.KNIGHT:
                piece_value = 320
            elif piece.piece_type == chess.BISHOP:
                piece_value = 330
            elif piece.piece_type == chess.ROOK:
                piece_value = 500
            elif piece.piece_type == chess.QUEEN:
                piece_value = 900
            elif piece.piece_type == chess.KING:
                piece_value = 20000
            if piece.color == chess.WHITE:
                material_score += piece_value
            else:
                material_score -= piece_value
    return material_score