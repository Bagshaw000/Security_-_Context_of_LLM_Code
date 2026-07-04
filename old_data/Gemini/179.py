



def calculate_score(fen_string):
    
    
    
    
    piece_values = {
        'P': 1,   
        'N': 3,   
        'B': 3,   
        'R': 5,   
        'Q': 9,   
        'K': 0,   
        'p': -1,  
        'n': -3,  
        'b': -3,  
        'r': -5,  
        'q': -9,  
        'k': 0    
    }

    total_score = 0

    
    
    for character in fen_string:
        
        if character in piece_values:
            total_score = total_score + piece_values[character]
            
    return total_score



starting_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
score1 = calculate_score(starting_position)



white_winning = "rnb1kbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
score2 = calculate_score(white_winning)


print("Chess Position Evaluation")
print("-------------------------")
print("Starting Position Score:", score1)
print("Score if Black loses a Queen:", score2)
print("")
print("Guide:")
print("A positive score means White has more material.")
print("A negative score means Black has more material.")
print("A score of 0 means the material is perfectly even.")