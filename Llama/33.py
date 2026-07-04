import chess

def evaluate_position(board):
    
    score = 0
    
    
    for i in range(8):
        if board[i] == 'wp':  
            if i < 3:
                score += 10
            elif i > 4:
                score -= 9
        elif board[i] == 'bp':  
            if i < 3:
                score -= 10
            elif i > 4:
                score += 9
    
    
    for i in range(8):
        if board[i] == 'wpk':  
            score += 3
        elif board[i] == 'bpk':  
            score -= 3
        elif board[i] == 'wbr':  
            score += 3
        elif board[i] == 'bbr':  
            score -= 3
        elif board[i] == 'wpq':  
            score += 9
        elif board[i] == 'bpq':  
            score -= 9
        elif board[i] == 'wkr':  
            score += 5
        elif board[i] == 'bkr':  
            score -= 5
        elif board[i] == 'wpn' or board[i] == 'bpn':  
            score += 50
    
    return score


board = chess.pgn.read_board_string('1. e4 e5 2. Nf3 Nc6 3. Bb5')
print(evaluate_position(board))