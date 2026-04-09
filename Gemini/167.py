import chess
import unittest

class ChessPositionEvaluator:
    

    
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

    def __init__(self):
        pass

    def evaluate(self, board: chess.Board) -> int:
        
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -100000  
            else:
                return 100000   

        if board.is_stalemate() or board.is_insufficient_material() or board.is_seventyfive_moves():
            return 0

        score = 0
        
        
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                value = self.PIECE_VALUES.get(piece.piece_type, 0)
                
                
                pst_bonus = 0
                if piece.piece_type == chess.PAWN:
                    
                    if piece.color == chess.WHITE:
                        pst_bonus = self.PAWN_PST[chess.square_mirror(square)]
                    else:
                        pst_bonus = self.PAWN_PST[square]

                if piece.color == chess.WHITE:
                    score += (value + pst_bonus)
                else:
                    score -= (value + pst_bonus)

        return score

class TestChessEvaluator(unittest.TestCase):
    

    def setUp(self):
        self.evaluator = ChessPositionEvaluator()
        self.board = chess.Board()

    def test_starting_position(self):
        
        score = self.evaluator.evaluate(self.board)
        self.assertEqual(score, 0)

    def test_material_advantage(self):
        
        self.board.remove_piece_at(chess.D8)
        score = self.evaluator.evaluate(self.board)
        self.assertGreater(score, 800)

    def test_scholar_mate_score(self):
        
        moves = ["e4", "e5", "Qh5", "Nc6", "Bc4", "Nf6", "Qxf7"]
        for move in moves:
            self.board.push_san(move)
        score = self.evaluator.evaluate(self.board)
        self.assertEqual(score, 100000)

if __name__ == "__main__":
    
    print("Initializing Chess Position Evaluator...")
    
    
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChessEvaluator)
    unittest.TextTestRunner(verbosity=2).run(suite)

    
    example_board = chess.Board()
    evaluator = ChessPositionEvaluator()
    print(f"\nCurrent Board FEN: {example_board.fen()}")
    print(f"Static Evaluation: {evaluator.evaluate(example_board)}")
    
    
    example_board.push_san("e4")
    print(f"Evaluation after 1. e4: {evaluator.evaluate(example_board)}")