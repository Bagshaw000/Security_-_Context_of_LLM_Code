import chess

def evaluate_position(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -10000
        else:
            return 10000
    elif board.is_stalemate():
        return 0
    else:
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }
        
        score = 0
        for square in range(64):
            piece = board.piece_at(square)
            if piece:
                score += piece_values[piece.piece_type] * (1 if piece.color == chess.WHITE else -1)
        
        return score