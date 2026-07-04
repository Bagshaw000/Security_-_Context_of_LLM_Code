


import chess



def evaluate_chess_board(position_code):
    
    board = chess.Board(position_code)
    
    
    
    points_map = {
        chess.PAWN: 1,
        chess.KNIGHT: 3,
        chess.BISHOP: 3,
        chess.ROOK: 5,
        chess.QUEEN: 9,
        chess.KING: 0  
    }
    
    total_score = 0
    
    
    for square in chess.SQUARES:
        piece = board.piece_at(square)
        
        
        if piece is not None:
            value = points_map[piece.piece_type]
            
            
            
            if piece.color == chess.WHITE:
                total_score = total_score + value
            else:
                total_score = total_score - value
                
    return total_score



sample_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


final_evaluation = evaluate_chess_board(sample_position)


print("Chess Position Analysis")
print("-----------------------")
print("Total Score:", final_evaluation)

if final_evaluation > 0:
    print("Conclusion: White has more material value.")
elif final_evaluation < 0:
    print("Conclusion: Black has more material value.")
else:
    print("Conclusion: The material is perfectly balanced.")


