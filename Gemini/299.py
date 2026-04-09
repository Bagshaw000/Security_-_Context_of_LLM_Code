

guesses = ["Cat", "Cat", "Dog", "Cat", "Bird"]

def find_most_likely_answer(list_of_guesses):
    
    tally = {}
    
    for word in list_of_guesses:
        if word in tally:
            
            tally[word] = tally[word] + 1
        else:
            
            tally[word] = 1
            
    
    winner = max(tally, key=tally.get)
    
    
    
    votes_for_winner = tally[winner]
    total_votes = len(list_of_guesses)
    confidence_percentage = (votes_for_winner / total_votes) * 100
    
    return winner, confidence_percentage


final_answer, confidence = find_most_likely_answer(guesses)

print("The most likely classification is: " + str(final_answer))
print("The confidence level is: " + str(confidence) + "%")