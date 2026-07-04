def evaluate_chess_position(board):
    
    
    piece_values = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}
    
    
    score = 0
    
    
    for row in board:
        for square in row:
            
            if square != '-':
                
                piece = square[1]
                color = square[0]
                
                
                if color == 'w':
                    score += piece_values[piece]
                else:
                    score -= piece_values[piece]
    
    return score