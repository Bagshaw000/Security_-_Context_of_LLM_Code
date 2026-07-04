import chess

class ChessEvaluator:
    

    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    
    
    PST = {
        chess.PAWN: [
            0,  0,  0,  0,  0,  0,  0,  0,
            50, 50, 50, 50, 50, 50, 50, 50,
            10, 10, 20, 30, 30, 20, 10, 10,
            5,  5, 10, 25, 25, 10,  5,  5,
            0,  0,  0, 20, 20,  0,  0,  0,
            5, -5,-10,  0,  0,-10, -5,  5,
            5, 10, 10,-20,-20, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ],
        chess.KNIGHT: [
            -50,-40,-30,-30,-30,-30,-40,-50,
            -40,-20,  0,  0,  0,  0,-20,-40,
            -30,  0, 10, 15, 15, 10,  0,-30,
            -30,  5, 15, 20, 20, 15,  5,-30,
            -30,  0, 15, 20, 20, 15,  0,-30,
            -30,  5, 10, 15, 15, 10,  5,-30,
            -40,-20,  0,  5,  5,  0,-20,-40,
            -50,-40,-30,-30,-30,-30,-40,-50
        ],
        chess.BISHOP: [
            -20,-10,-10,-10,-10,-10,-10,-20,
            -10,  0,  0,  0,  0,  0,  0,-10,
            -10,  0,  5, 10, 10,  5,  0,-10,
            -10,  5,  5, 10, 10,  5,  5,-10,
            -10,  0, 10, 10, 10, 10,  0,-10,
            -10, 10, 10, 10, 10, 10, 10,-10,
            -10,  5,  0,  0,  0,  0,  5,-10,
            -20,-10,-10,-10,-10,-10,-10,-20
        ],
        chess.ROOK: [
            0,  0,  0,  5,  5,  0,  0,  0,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            5, 10, 10, 10, 10, 10, 10,  5,
            0,  0,  0,  0,  0,  0,  0,  0
        ]
    }

    def evaluate(self, board: chess.Board) -> int:
        
        if board.is_checkmate():
            return -200000 if board.turn == chess.WHITE else 200000
        
        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        piece_map = board.piece_map()

        
        for square, piece in piece_map.items():
            value = self.PIECE_VALUES.get(piece.piece_type, 0)
            
            
            pst_table = self.PST.get(piece.piece_type)
            if pst_table:
                
                
                idx = chess.square_mirror(square) if piece.color == chess.WHITE else square
                value += pst_table[idx]

            if piece.color == chess.WHITE:
                score += value
            else:
                score -= value

        
        
        white_mobility, black_mobility = self._get_mobility_scores(board)
        score += (white_mobility - black_mobility) * 10

        return score

    def _get_mobility_scores(self, board: chess.Board) -> (int, int):
        
        original_turn = board.turn
        
        board.turn = chess.WHITE
        w_moves = board.legal_moves.count()
        
        board.turn = chess.BLACK
        b_moves = board.legal_moves.count()
        
        board.turn = original_turn
        return w_moves, b_moves

def analyze_fen(fen_string: str):
    
    board = chess.Board(fen_string)
    evaluator = ChessEvaluator()
    result = evaluator.evaluate(board)
    print(f"Position: {fen_string}")
    print(f"Static Evaluation: {result}")

if __name__ == "__main__":
    
    starting_board = chess.Board()
    engine = ChessEvaluator()
    print(f"Starting Position Score: {engine.evaluate(starting_board)}")
    
    
    e4_board = chess.Board("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1")
    print(f"Evaluation after 1. e4: {engine.evaluate(e4_board)}")