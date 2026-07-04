





piece_points = {
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





chess_board = 



total_score = 0


for character in chess_board:
    
    if character in piece_points:
        total_score = total_score + piece_points[character]


print("Chess Evaluation Summary")
print("------------------------")
print("Material Score:", total_score)

if total_score > 0:
    print("Result: White has the advantage.")
elif total_score < 0:
    print("Result: Black has the advantage.")
else:
    print("Result: The position is even.")