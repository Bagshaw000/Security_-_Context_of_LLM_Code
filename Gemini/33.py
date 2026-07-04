import chess
import unittest

class ChessEvaluator:
    
    
    
    PIECE_VALUES = {
        chess.PAWN: 100,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.ROOK: 500,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    def __init__(self, fen: str = None):
        
        self.board = chess.Board(fen) if fen else chess.Board()

    def evaluate(self) -> int:
        
        if self.board.is_checkmate():
            
            return -30000 if self.board.turn == chess.WHITE else 30000
        
        if self.board.is_draw() or self.board.is_stalemate():
            return 0

        score = 0
        
        
        for piece_type, value in self.PIECE_VALUES.items():
            white_pieces = self.board.pieces(piece_type, chess.WHITE)
            black_pieces = self.board.pieces(piece_type, chess.BLACK)
            
            score += len(white_pieces) * value
            score -= len(black_pieces) * value

        return score

class TestChessEvaluator(unittest.TestCase):
    
    
    def test_starting_position(self):
        evaluator = ChessEvaluator()
        self.assertEqual(evaluator.evaluate(), 0)

    def test_white_advantage(self):
        
        board = chess.Board()
        board.remove_piece_at(chess.D8)
        evaluator = ChessEvaluator(board.fen())
        self.assertEqual(evaluator.evaluate(), 900)

    def test_black_advantage(self):
        
        board = chess.Board()
        board.remove_piece_at(chess.A1)
        evaluator = ChessEvaluator(board.fen())
        self.assertEqual(evaluator.evaluate(), -500)

    def test_checkmate_evaluation(self):
        
        fools_mate_fen = "rnb1kbnr/pppp1ppp/8/4p3/6Pq/5P2/PPPPP2P/RNBQKBNR w KQkq - 1 3"
        evaluator = ChessEvaluator(fools_mate_fen)
        self.assertEqual(evaluator.evaluate(), -30000)

def main():
    
    current_board = chess.Board()
    evaluator = ChessEvaluator()
    print(f"Starting Position Evaluation: {evaluator.evaluate()}")
    
    
    current_board.push_san("e4")
    evaluator = ChessEvaluator(current_board.fen())
    print(f"Evaluation after 1. e4: {evaluator.evaluate()}")

if __name__ == "__main__":
    
    main()
    
    
    
    unittest.main(exit=False)