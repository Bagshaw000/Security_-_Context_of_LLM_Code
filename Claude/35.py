import chess

def evaluate_position(fen):
    board = chess.Board(fen)
    
    
    evaluation = 0
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.color == chess.WHITE:
                evaluation += piece.piece_type
            else:
                evaluation -= piece.piece_type
    
    return evaluation