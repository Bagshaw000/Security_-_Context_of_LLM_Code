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

    
    
    PAWN_PST = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    KNIGHT_PST = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50
    ]

    BISHOP_PST = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20
    ]

    def __init__(self, board: chess.Board):
        self.board = board

    def evaluate(self) -> int:
        
        if self.board.is_checkmate():
            return -99999 if self.board.turn == chess.WHITE else 99999
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        material_score = self._calculate_material()
        positional_score = self._calculate_positional()
        
        return material_score + positional_score

    def _calculate_material(self) -> int:
        score = 0
        for piece_type, value in self.PIECE_VALUES.items():
            score += len(self.board.pieces(piece_type, chess.WHITE)) * value
            score -= len(self.board.pieces(piece_type, chess.BLACK)) * value
        return score

    def _calculate_positional(self) -> int:
        score = 0
        
        score += self._sum_pst(chess.PAWN, chess.WHITE, self.PAWN_PST)
        score += self._sum_pst(chess.KNIGHT, chess.WHITE, self.KNIGHT_PST)
        score += self._sum_pst(chess.BISHOP, chess.WHITE, self.BISHOP_PST)
        
        
        score -= self._sum_pst(chess.PAWN, chess.BLACK, self.PAWN_PST[::-1])
        score -= self._sum_pst(chess.KNIGHT, chess.BLACK, self.KNIGHT_PST[::-1])
        score -= self._sum_pst(chess.BISHOP, chess.BLACK, self.BISHOP_PST[::-1])
        
        return score

    def _sum_pst(self, piece_type: chess.PieceType, color: chess.Color, pst: list) -> int:
        score = 0
        for square in self.board.pieces(piece_type, color):
            
            score += pst[square]
        return score


if __name__ == "__main__":
    
    board = chess.Board()
    
    
    board.push_san("e4")
    board.push_san("e5")
    board.push_san("Nf3")
    
    evaluator = ChessEvaluator(board)
    current_eval = evaluator.evaluate()
    
    print(f"FEN: {board.fen()}")
    print(f"Position Evaluation: {current_eval} (Positive favors White)")