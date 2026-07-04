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
             0,  0,  0,  0,  0,  0,  0,  0,
             5, 10, 10, 10, 10, 10, 10,  5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
            -5,  0,  0,  0,  0,  0,  0, -5,
             0,  0,  0,  5,  5,  0,  0,  0
        ]
    }

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
            
            piece_type = piece.piece_type
            piece_color = piece.color
            
            
            value = self.PIECE_VALUES.get(piece_type, 0)
            
            
            if piece_type in self.PST:
                
                idx = square if piece_color == chess.WHITE else chess.square_mirror(square)
                value += self.PST[piece_type][idx]
            
            
            if piece_color == chess.WHITE:
                score += value
            else:
                score -= value
        
        return score

def main():
    
    board = chess.Board()
    evaluator = ChessEvaluator()
    
    
    initial_score = evaluator.evaluate(board)
    print(f"Initial Position Score: {initial_score}")

    
    board.push_san("e4")
    e4_score = evaluator.evaluate(board)
    print(f"Score after 1. e4: {e4_score}")

    
    board.push_san("e5")
    e5_score = evaluator.evaluate(board)
    print(f"Score after 1... e5: {e5_score}")

if __name__ == "__main__":
    main()