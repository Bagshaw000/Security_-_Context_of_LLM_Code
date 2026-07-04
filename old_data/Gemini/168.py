import chess


PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_position(board: chess.Board) -> int:
    
    
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999  
        else:
            return 99999   
            
    if board.is_stalemate() or board.is_insufficient_material():
        return 0

    total_evaluation = 0
    
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            value = PIECE_VALUES.get(piece.piece_type, 0)
            if piece.color == chess.WHITE:
                total_evaluation += value
            else:
                total_evaluation -= value
                
    return total_evaluation

def run_unit_tests():
    
    
    board = chess.Board()
    assert evaluate_position(board) == 0
    
    
    board.remove_piece_at(chess.E7)
    assert evaluate_position(board) == 100
    
    
    board = chess.Board()
    board.remove_piece_at(chess.D1)
    assert evaluate_position(board) == -900
    
    print("Unit tests passed.")

if __name__ == "__main__":
    
    current_board = chess.Board()
    score = evaluate_position(current_board)
    print(f"Board Evaluation (Starting Position): {score}")
    
    
    run_unit_tests()