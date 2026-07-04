import chess

def evaluate_position(board):
    
    material_score = 0
    for square in range(64):
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                if piece.piece_type == chess.PAWN:
                    material_score += 1
                elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                    material_score += 3
                elif piece.piece_type == chess.ROOK:
                    material_score += 5
                elif piece.piece_type == chess.QUEEN:
                    material_score += 9
            else:
                if piece.piece_type == chess.PAWN:
                    material_score -= 1
                elif piece.piece_type == chess.KNIGHT or piece.piece_type == chess.BISHOP:
                    material_score -= 3
                elif piece.piece_type == chess.ROOK:
                    material_score -= 5
                elif piece.piece_type == chess.QUEEN:
                    material_score -= 9
    return material_score


board = chess.Board()
board.push_san("e4")
board.push_san("e5")
board.push_san("Nf3")
board.push_san("Nc6")
print(evaluate_position(board))