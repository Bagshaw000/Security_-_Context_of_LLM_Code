import chess
import unittest

class ChessEvaluator:
    

    def __init__(self):
        
        self.piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 320,
            chess.BISHOP: 330,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 20000
        }

        
        
        self.pawn_pst = [
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10,-20,-20, 10, 10,  5,
             5, -5,-10,  0,  0,-10, -5,  5,
             0,  0,  0, 20, 20,  0,  0,  0,
             5,  5, 10, 25, 25, 10,  5,  5,
            10, 10, 20, 30, 30, 20, 10, 10,
            50, 50, 50, 50, 50, 50, 50, 50,
             0,  0,  0,  0,  0,  0,  0,  0
        ]

    def evaluate(self, board: chess.Board) -> int:
        
        if board.is_checkmate():
            return -99999 if board.turn == chess.WHITE else 99999

        if board.is_stalemate() or board.is_insufficient_material():
            return 0

        score = 0
        
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if not piece:
                continue

            
            value = self.piece_values[piece.piece_type]
            
            
            pst_bonus = 0
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    pst_bonus = self.pawn_pst[square]
                else:
                    
                    pst_bonus = self.pawn_pst[chess.square_mirror(square)]

            if piece.color == chess.WHITE:
                score += (value + pst_bonus)
            else:
                score -= (value + pst_bonus)

        return score

class TestChessEvaluator(unittest.TestCase):
    
    def setUp(self):
        self.evaluator = ChessEvaluator()

    def test_initial_position(self):
        board = chess.Board()
        
        self.assertEqual(self.evaluator.evaluate(board), 0)

    def test_white_material_advantage(self):
        board = chess.Board()
        
        board.remove_piece_at(chess.D8)
        score = self.evaluator.evaluate(board)
        self.assertGreater(score, 800)

    def test_black_material_advantage(self):
        board = chess.Board()
        
        board.remove_piece_at(chess.A1)
        score = self.evaluator.evaluate(board)
        self.assertLess(score, -400)

    def test_pawn_progression_bonus(self):
        
        board_start = chess.Board(fen="8/8/8/8/8/8/P7/8 w - - 0 1")
        board_advanced = chess.Board(fen="8/P7/8/8/8/8/8/8 w - - 0 1")
        
        score_start = self.evaluator.evaluate(board_start)
        score_advanced = self.evaluator.evaluate(board_advanced)
        
        self.assertGreater(score_advanced, score_start)

if __name__ == "__main__":
    
    evaluator = ChessEvaluator()
    sample_board = chess.Board()
    
    print(f"Current Evaluation (Starting Position): {evaluator.evaluate(sample_board)}")
    
    
    print("\nRunning automated tests...")
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChessEvaluator)
    unittest.TextTestRunner(verbosity=1).run(suite)