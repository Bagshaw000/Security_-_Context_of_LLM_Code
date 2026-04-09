import chess

def evaluate_position(board):
    
    
    
    
    
    
    material_score = 0
    for piece in chess.PIECE_TYPES:
        material_score += len(board.pieces(piece, chess.WHITE)) * chess.piece_values[piece]
        material_score -= len(board.pieces(piece, chess.BLACK)) * chess.piece_values[piece]
    
    return material_score