import chess

def evaluate_position(board):
    
    
    
    material_score = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                if piece.piece_type == chess.PAWN:
                    material_score += 100
                elif piece.piece_type == chess.KNIGHT:
                    material_score += 300
                elif piece.piece_type == chess.BISHOP:
                    material_score += 330
                elif piece.piece_type == chess.ROOK:
                    material_score += 500
                elif piece.piece_type == chess.QUEEN:
                    material_score += 900
                elif piece.piece_type == chess.KING:
                    material_score += 20000
            else:
                if piece.piece_type == chess.PAWN:
                    material_score -= 100
                elif piece.piece_type == chess.KNIGHT:
                    material_score -= 300
                elif piece.piece_type == chess.BISHOP:
                    material_score -= 330
                elif piece.piece_type == chess.ROOK:
                    material_score -= 500
                elif piece.piece_type == chess.QUEEN:
                    material_score -= 900
                elif piece.piece_type == chess.KING:
                    material_score -= 20000
    return material_score