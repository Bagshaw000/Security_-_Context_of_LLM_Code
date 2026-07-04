

guesses_from_networks = ["Cat", "Cat", "Dog", "Cat", "Bird"]



def calculate_majority_vote(list_of_guesses):
    
    tally = {}
    for guess in list_of_guesses:
        if guess in tally:
            
            tally[guess] = tally[guess] + 1
        else:
            
            tally[guess] = 1
    
    
    best_guess = max(tally, key=tally.get)
    
    
    votes_for_winner = tally[best_guess]
    total_votes = len(list_of_guesses)
    confidence = (votes_for_winner / total_votes) * 100
    
    return best_guess, confidence


final_answer, confidence_score = calculate_majority_vote(guesses_from_networks)


print("The most likely classification is: " + str(final_answer))
print("The confidence level is: " + str(confidence_score) + "%")