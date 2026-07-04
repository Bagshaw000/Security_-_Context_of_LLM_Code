import chess

def evaluate_position(board):
    
    board = chess.Board(board)

    
    evaluation = board.evaluate()

    return evaluation