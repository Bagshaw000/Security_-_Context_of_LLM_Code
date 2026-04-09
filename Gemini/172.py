import chess

class ChessPositionEvaluator:
    

    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    
    
    PST_PAWN = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0
    ]

    PST_KNIGHT = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50,
    ]

    PST_BISHOP = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20,
    ]

    def __init__(self, board: chess.Board):
        self.board = board

    def get_evaluation(self) -> float:
        
        if self.board.is_checkmate():
            return -99999 if self.board.turn == chess.WHITE else 99999
        
        if self.board.is_stalemate() or self.board.is_insufficient_material():
            return 0

        score = 0
        score += self._evaluate_material()
        score += self._evaluate_positioning()
        
        return score

    def _evaluate_material(self) -> int:
        
        score = 0
        for piece_type, value in self.PIECE_VALUES.items():
            score += len(self.board.pieces(piece_type, chess.WHITE)) * value
            score -= len(self.board.pieces(piece_type, chess.BLACK)) * value
        return score

    def _evaluate_positioning(self) -> int:
        
        score = 0
        
        
        for square in self.board.pieces(chess.PAWN, chess.WHITE):
            score += self.PST_PAWN[chess.square_mirror(square)]
        for square in self.board.pieces(chess.KNIGHT, chess.WHITE):
            score += self.PST_KNIGHT[chess.square_mirror(square)]
        for square in self.board.pieces(chess.BISHOP, chess.WHITE):
            score += self.PST_BISHOP[chess.square_mirror(square)]

        
        for square in self.board.pieces(chess.PAWN, chess.BLACK):
            score -= self.PST_PAWN[square]
        for square in self.board.pieces(chess.KNIGHT, chess.BLACK):
            score -= self.PST_KNIGHT[square]
        for square in self.board.pieces(chess.BISHOP, chess.BLACK):
            score -= self.PST_BISHOP[square]

        return score

def main():
    
    board = chess.Board()
    
    
    moves = ["e4", "e5", "Nf3"]
    for move in moves:
        board.push_san(move)
    
    evaluator = ChessPositionEvaluator(board)
    current_score = evaluator.get_evaluation()
    
    print(f"Current FEN: {board.fen()}")
    print(f"Evaluation Score (Centipawns): {current_score}")
    
    if current_score > 0:
        print("Status: White has a positional advantage.")
    elif current_score < 0:
        print("Status: Black has a positional advantage.")
    else:
        print("Status: The position is balanced.")

if __name__ == "__main__":
    main()