


guesses = ["Apple", "Apple", "Orange", "Apple", "Banana"]

def determine_final_classification(list_of_guesses):
    
    total_number_of_guesses = len(list_of_guesses)
    
    
    
    best_guess = max(set(list_of_guesses), key=list_of_guesses.count)
    
    
    votes_for_best_guess = list_of_guesses.count(best_guess)
    
    
    
    confidence_level = (votes_for_best_guess / total_number_of_guesses) * 100
    
    return best_guess, confidence_level


final_result, confidence_score = determine_final_classification(guesses)


print("The most likely classification is: " + str(final_result))
print("The confidence level is: " + str(round(confidence_score, 2)) + "%")