import chess



MATERIAL_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

def evaluate_position(board: chess.Board) -> int:
    
    
    if board.is_checkmate():
        
        return -99999 if board.turn == chess.WHITE else 99999
    
    if board.is_draw():
        return 0

    score = 0

    
    for piece_type in MATERIAL_VALUES:
        white_count = len(board.pieces(piece_type, chess.WHITE))
        black_count = len(board.pieces(piece_type, chess.BLACK))
        
        score += white_count * MATERIAL_VALUES[piece_type]
        score -= black_count * MATERIAL_VALUES[piece_type]

    
    
    mobility_bonus = board.legal_moves.count()
    if board.turn == chess.WHITE:
        score += mobility_bonus
    else:
        score -= mobility_bonus

    return score

def run_basic_tests():
    
    
    board = chess.Board()
    
    assert evaluate_position(board) == 20
    
    
    board.remove_piece_at(chess.E7)
    assert evaluate_position(board) > 100
    
    
    board = chess.Board()
    board.remove_piece_at(chess.D1)
    assert evaluate_position(board) < -800

    print("All basic evaluation tests passed.")

if __name__ == "__main__":
    
    
    sample_fen = "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
    chess_board = chess.Board(sample_fen)
    
    eval_score = evaluate_position(chess_board)
    print(f"Evaluation for FEN: {sample_fen}")
    print(f"Score: {eval_score}")
    
    run_basic_tests()