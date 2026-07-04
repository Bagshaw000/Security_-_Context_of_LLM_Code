import chess
import re
from typing import Union

def evaluate_chess_position(fen: str) -> Union[float, str]:
    
    
    if not isinstance(fen, str):
        return "Error: Input must be a string."

    
    
    if len(fen) > 128:
        return "Error: FEN string exceeds maximum allowed length."

    
    
    
    safe_pattern = re.compile(r"^[a-zA-Z0-9/\-\s]+$")
    if not safe_pattern.match(fen):
        return "Error: FEN contains illegal characters."

    try:
        
        
        board = chess.Board(fen)

        
        
        if not board.is_valid():
            return "Error: FEN represents an illegal board state."

        
        
        
        piece_values = {
            chess.PAWN: 1.0,
            chess.KNIGHT: 3.2,
            chess.BISHOP: 3.3,
            chess.ROOK: 5.0,
            chess.QUEEN: 9.0,
            chess.KING: 0.0  
        }

        material_balance = 0.0

        for piece_type, value in piece_values.items():
            
            white_count = len(board.pieces(piece_type, chess.WHITE))
            
            black_count = len(board.pieces(piece_type, chess.BLACK))
            
            material_balance += (white_count - black_count) * value

        return round(material_balance, 2)

    except ValueError:
        return "Error: FEN format is invalid."
    except Exception:
        
        return "Error: An internal error occurred during evaluation."


if __name__ == "__main__":
    
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    print(f"Material Score: {evaluate_chess_position(starting_fen)}")