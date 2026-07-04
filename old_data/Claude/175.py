import chess

def evaluate_position(fen):
    board = chess.Board(fen)
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return float('-inf')
        else:
            return float('inf')
    elif board.is_stalemate() or board.is_insufficient_material() or board.is_threefold_repetition():
        return 0.0
    else:
        
        
        white_material = board.piece_count(chess.WHITE)
        black_material = board.piece_count(chess.BLACK)
        return white_material - black_material