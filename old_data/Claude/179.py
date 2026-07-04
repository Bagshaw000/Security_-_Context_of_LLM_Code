import chess

def evaluate_position(fen):
    board = chess.Board(fen)
    if board.is_checkmate():
        return -10000 if board.turn == chess.WHITE else 10000
    elif board.is_stalemate():
        return 0
    else:
        return board.material_count(chess.WHITE) - board.material_count(chess.BLACK)