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

    score = 0
    
    
    for piece_type in PIECE_VALUES:
        
        score += len(board.pieces(piece_type, chess.WHITE)) * PIECE_VALUES[piece_type]
        
        score -= len(board.pieces(piece_type, chess.BLACK)) * PIECE_VALUES[piece_type]

    
    
    mobility_weight = 10
    if board.turn == chess.WHITE:
        score += board.legal_moves.count() * mobility_weight
    else:
        
        board.turn = chess.WHITE
        score -= board.legal_moves.count() * mobility_weight
        board.turn = chess.BLACK

    return score

def run_basic_test():
    
    board = chess.Board()
    
    
    
    initial_eval = evaluate_position(board)
    print(f"Initial Position Eval: {initial_eval}")
    
    
    
    board.set_fen("rnbqkbnr/pppp1ppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")
    pawn_up_eval = evaluate_position(board)
    print(f"White up a pawn eval: {pawn_up_eval}")
    
    assert pawn_up_eval > 0, "White should have a positive score when up material"

if __name__ == "__main__":
    run_basic_test()