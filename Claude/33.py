import chess

def evaluate_chess_position(board):
    
    
    score = 0
    
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.color == chess.WHITE:
                score += piece_value(piece.piece_type)
            else:
                score -= piece_value(piece.piece_type)
    
    return score

def piece_value(piece_type):
    
    if piece_type == chess.PAWN:
        return 100
    elif piece_type == chess.KNIGHT or piece_type == chess.BISHOP:
        return 300
    elif piece_type == chess.ROOK:
        return 500
    elif piece_type == chess.QUEEN:
        return 900
    elif piece_type == chess.KING:
        return 10000
    else:
        return 0